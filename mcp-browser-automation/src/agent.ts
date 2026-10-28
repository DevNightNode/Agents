import { chromium } from 'playwright';
import { z } from 'zod';
import fs from 'fs';
import path from 'path';

export class BrowserAutomationAgent {
  private browser: any;
  private page: any;
  private context: any;

  constructor() {
    // Initialize the browser when the agent is created
  }

  async init() {
    this.browser = await chromium.launch({ headless: true });
    this.context = await this.browser.newContext();
    this.page = await this.context.newPage();
  }

  async navigate(url: string): Promise<string> {
    if (!this.page) {
      await this.init();
    }
    try {
      await this.page.goto(url, { waitUntil: 'networkidle' });
      return `Navigated to ${url}`;
    } catch (error) {
      return `Failed to navigate to ${url}: ${error}`;
    }
  }

  async click(selector: string): Promise<string> {
    if (!this.page) {
      await this.init();
    }
    try {
      await this.page.click(selector);
      return `Clicked on element with selector: ${selector}`;
    } catch (error) {
      return `Failed to click on element with selector ${selector}: ${error}`;
    }
  }

  async fill(selector: string, text: string): Promise<string> {
    if (!this.page) {
      await this.init();
    }
    try {
      await this.page.fill(selector, text);
      return `Filled element with selector ${selector} with text: ${text}`;
    } catch (error) {
      return `Failed to fill element with selector ${selector}: ${error}`;
    }
  }

  async screenshot(path?: string): Promise<string> {
    if (!this.page) {
      await this.init();
    }
    try {
      const screenshotBuffer = await this.page.screenshot({ fullPage: true });
      const base64Data = screenshotBuffer.toString('base64');
      if (path) {
        const screenshotPath = path;
        fs.writeFileSync(screenshotPath, screenshotBuffer);
        return `Screenshot saved to ${screenshotPath}`;
      }
      return `Screenshot (base64): ${base64Data}`;
    } catch (error) {
      return `Failed to take screenshot: ${error}`;
    }
  }

  async getText(selector: string): Promise<string> {
    if (!this.page) {
      await this.init();
    }
    try {
      const text = await this.page.textContent(selector);
      return text || '';
    } catch (error) {
      return `Failed to extract text from element with selector ${selector}: ${error}`;
    }
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}
