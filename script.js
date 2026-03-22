/**
 * SalaryWiseCalc - Calculator logic
 * Converts hourly ↔ yearly, with basic tax estimation
 */

(function () {
  'use strict';

  const HOURS_PER_WEEK = 40;
  const WEEKS_PER_YEAR = 52;

  // Simplified tax rates (approximate federal + typical state avg, US)
  function getTaxRate(annualGross) {
    if (annualGross <= 11000) return 0.10;
    if (annualGross <= 44725) return 0.12;
    if (annualGross <= 95375) return 0.22;
    if (annualGross <= 182100) return 0.24;
    if (annualGross <= 231250) return 0.32;
    if (annualGross <= 578125) return 0.35;
    return 0.37;
  }

  function formatCurrency(num) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(num);
  }

  function calculateHourlyFromYearly(yearly) {
    const hoursPerYear = HOURS_PER_WEEK * WEEKS_PER_YEAR;
    return yearly / hoursPerYear;
  }

  function calculateYearlyFromHourly(hourly) {
    return hourly * HOURS_PER_WEEK * WEEKS_PER_YEAR;
  }

  function estimateTax(grossAnnual) {
    const rate = getTaxRate(grossAnnual);
    return grossAnnual * rate;
  }

  function initCalculator(container) {
    if (!container) return;

    const type = container.dataset.calculator;
    const hourlyInput = container.querySelector('[data-input="hourly"]');
    const yearlyInput = container.querySelector('[data-input="yearly"]');

    const outGrossYearly = container.querySelector('[data-output="gross-yearly"]');
    const outGrossHourly = container.querySelector('[data-output="gross-hourly"]');
    const outTax = container.querySelector('[data-output="tax-estimate"]');
    const outNet = container.querySelector('[data-output="net-yearly"]');

    let isUpdating = false;
    let lastEdited = 'hourly';

    function update(source) {
      if (isUpdating) return;
      if (source) lastEdited = source;
      isUpdating = true;

      let hourly = parseFloat(hourlyInput?.value) || 0;
      let yearly = parseFloat(yearlyInput?.value) || 0;

      if (type === 'hourly-to-salary' && hourly > 0) {
        yearly = calculateYearlyFromHourly(hourly);
      } else if (type === 'salary-to-hourly' && yearly > 0) {
        hourly = calculateHourlyFromYearly(yearly);
      } else if (type === 'main') {
        if (lastEdited === 'hourly' && hourly > 0) {
          yearly = calculateYearlyFromHourly(hourly);
          yearlyInput.value = Math.round(yearly);
        } else if (yearly > 0) {
          hourly = calculateHourlyFromYearly(yearly);
          hourlyInput.value = hourly.toFixed(2);
        }
      }

      const grossAnnual = yearly || (hourly > 0 ? calculateYearlyFromHourly(hourly) : 0);
      const taxAmount = estimateTax(grossAnnual);
      const netAnnual = grossAnnual - taxAmount;

      if (outGrossYearly) outGrossYearly.textContent = formatCurrency(grossAnnual);
      if (outGrossHourly) outGrossHourly.textContent = formatCurrency(hourly);
      if (outTax) outTax.textContent = formatCurrency(taxAmount);
      if (outNet) outNet.textContent = formatCurrency(netAnnual);

      isUpdating = false;
    }

    if (hourlyInput) hourlyInput.addEventListener('input', () => update('hourly'));
    if (yearlyInput) yearlyInput.addEventListener('input', () => update('yearly'));

    update();
  }

  document.querySelectorAll('[data-calculator]').forEach(initCalculator);
})();
