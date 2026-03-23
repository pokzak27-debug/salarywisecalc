/**
 * SalaryWiseCalc - Shared salary conversion & formatting
 * Used by calculators for hourly ↔ yearly ↔ monthly ↔ weekly
 */
(function (global) {
  'use strict';

  const HOURS_PER_WEEK = 40;
  const WEEKS_PER_YEAR = 52;

  const salaryHelper = {
    HOURS_PER_WEEK,
    WEEKS_PER_YEAR,

    /** Annual hours (full-time equivalent) */
    get annualHours() {
      return HOURS_PER_WEEK * WEEKS_PER_YEAR;
    },

    /** Hourly → yearly gross */
    yearlyFromHourly(hourly) {
      return hourly * this.annualHours;
    },

    /** Yearly → hourly */
    hourlyFromYearly(yearly) {
      return yearly / this.annualHours;
    },

    /** Yearly → monthly */
    monthlyFromYearly(yearly) {
      return yearly / 12;
    },

    /** Yearly → weekly */
    weeklyFromYearly(yearly) {
      return yearly / WEEKS_PER_YEAR;
    },

    /** Hourly → weekly (40 hrs) */
    weeklyFromHourly(hourly) {
      return hourly * HOURS_PER_WEEK;
    },

    /** Format number with currency symbol (no decimals unless needed) */
    formatAmount(value, symbol) {
      if (value === null || value === undefined || isNaN(value)) return '—';
      const formatted = new Intl.NumberFormat('en', {
        maximumFractionDigits: 0,
        minimumFractionDigits: 0
      }).format(Math.round(value));
      return symbol ? `${symbol}${formatted}`.replace(/\$\$/g, symbol) : formatted;
    },

    /** Format for common currency symbols (₦, ₱, KES, R, etc.) */
    formatCurrency(value, opts) {
      opts = opts || {};
      const symbol = opts.symbol || opts.currency || '$';
      const position = opts.position || 'before'; // 'before' | 'after'
      const decimals = opts.decimals ?? 0;
      if (value === null || value === undefined || isNaN(value)) return '—';
      const formatted = new Intl.NumberFormat('en', {
        maximumFractionDigits: decimals,
        minimumFractionDigits: decimals
      }).format(value);
      return position === 'after'
        ? `${formatted} ${symbol}`.trim()
        : `${symbol}${formatted}`;
    },

    /** Get formatter for Intl (USD style) */
    getFormatter(currency) {
      try {
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: currency || 'USD',
          maximumFractionDigits: 0
        });
      } catch (_) {
        return null;
      }
    }
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = salaryHelper;
  } else {
    global.SalaryHelper = salaryHelper;
  }
})(typeof window !== 'undefined' ? window : this);
