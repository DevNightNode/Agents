# Shopify Inventory Agent

A LangChain.js agent that manages Shopify store inventory, prices, and discount codes through the Shopify Admin API.

## Features

This agent can:
- Check inventory levels for specific products
- Update product prices for variants
- Create discount codes with various types and usage limits

## Tools

### `get_inventory`
Fetches inventory information for a specific product.

**Parameters:**
- `product_id` (string): The Shopify product ID to fetch inventory for

**Example:** `get_inventory({ product_id: "123456789" })`

### `update_price`
Updates the price of a specific product variant.

**Parameters:**
- `product_id` (string): The Shopify product ID
- `variant_id` (string): The variant ID to update
- `new_price` (number): The new price value

**Example:** `update_price({ product_id: "123456789", variant_id: "987654321", new_price: 29.99 })`

### `create_discount_code`
Creates a new discount code in Shopify.

**Parameters:**
- `code` (string): The discount code to create
- `value` (number): The discount value
- `type` (string): The type of discount ('percentage' or 'fixed_amount')
- `usage_limit` (number, optional): Maximum number of times the discount can be used

**Example:** `create_discount_code({ code: "SAVE10", value: 10, type: "percentage", usage_limit: 100 })`

## Required Environment Variables

Create a `.env` file with the following variables:

```env
SHOPIFY_SHOP_NAME=your-shop-name
SHOPIFY_ACCESS_TOKEN=your-access-token
OPENAI_API_KEY=your-openai-api-key
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Build the project:
```bash
npm run build
```

3. Run the agent:
```bash
npm start "Check inventory for product 123456789"
```

Or for development:
```bash
npm run dev "Update price for variant 987654321 to 29.99"
```

## Usage Examples

- `Check inventory for product 123456789`
- `Update price for product 123456789 variant 987654321 to 29.99`
- `Create a 15% discount code called SAVE15 with usage limit 50`
- `Create a $5 fixed amount discount code called FIVEOFF`

## Security Notes

- The agent uses Shopify's Admin API with a permanent access token
- All API calls are made directly to Shopify's servers
- Environment variables are used to store sensitive information
- No data is stored or logged by the agent itself
