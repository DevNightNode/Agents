import { tool } from 'ai';
import { z } from 'zod';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-04-10',
});

export const findCustomer = tool({
  description: 'Find a Stripe customer by email or customer ID',
  parameters: z.object({
    query: z.string().describe('Customer email or ID to search for'),
  }),
  execute: async ({ query }) => {
    try {
      const customers = await stripe.customers.list({
        email: query,
        limit: 1,
      });

      if (customers.data.length > 0) {
        return {
          success: true,
          customer: customers.data[0],
        };
      }

      // If no email match, try searching by ID
      try {
        const customer = await stripe.customers.retrieve(query);
        return {
          success: true,
          customer,
        };
      } catch (error) {
        return {
          success: false,
          error: 'Customer not found',
        };
      }
    } catch (error) {
      return {
        success: false,
        error: `Failed to search customers: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  },
});

export const listInvoices = tool({
  description: 'List invoices for a customer',
  parameters: z.object({
    customerId: z.string().describe('Stripe customer ID'),
    limit: z.number().optional().describe('Number of invoices to return (default: 10)'),
  }),
  execute: async ({ customerId, limit = 10 }) => {
    try {
      const invoices = await stripe.invoices.list({
        customer: customerId,
        limit,
      });

      return {
        success: true,
        invoices: invoices.data.map(invoice => ({
          id: invoice.id,
          status: invoice.status,
          amount: invoice.amount_paid,
          currency: invoice.currency,
          created: invoice.created,
          due_date: invoice.due_date,
          subscription: invoice.subscription,
        })),
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to list invoices: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  },
});

export const issueRefund = tool({
  description: 'Issue a refund for a specific invoice',
  parameters: z.object({
    invoiceId: z.string().describe('Stripe invoice ID to refund'),
    amount: z.number().optional().describe('Amount to refund (in cents). If not specified, refunds full amount.'),
  }),
  execute: async ({ invoiceId, amount }) => {
    try {
      const invoice = await stripe.invoices.retrieve(invoiceId);
      
      if (!invoice.payment_intent) {
        return {
          success: false,
          error: 'Invoice does not have a payment intent',
        };
      }

      const refund = await stripe.refunds.create({
        payment_intent:
          typeof invoice.payment_intent === 'string' ? invoice.payment_intent : invoice.payment_intent.id,
        amount: amount || undefined,
      });

      return {
        success: true,
        refund,
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to issue refund: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  },
});

export const cancelSubscription = tool({
  description: 'Cancel a subscription',
  parameters: z.object({
    subscriptionId: z.string().describe('Stripe subscription ID to cancel'),
    cancelAtPeriodEnd: z.boolean().optional().describe('Cancel at the end of the current billing period (default: true)'),
  }),
  execute: async ({ subscriptionId, cancelAtPeriodEnd = true }) => {
    try {
      const subscription = await stripe.subscriptions.update(subscriptionId, {
        cancel_at_period_end: cancelAtPeriodEnd,
      });

      return {
        success: true,
        subscription,
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to cancel subscription: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  },
});
