// Currency utility functions for Indian Rupee (INR)

export const CURRENCY_SYMBOL = '₹';
export const CURRENCY_CODE = 'INR';

/**
 * Format number in Indian numbering system (lakhs, crores)
 * Example: 1234567 → 12,34,567
 */
export function formatIndianNumber(num) {
  if (!num && num !== 0) return '0';
  
  const number = parseFloat(num);
  const [integerPart, decimalPart] = number.toFixed(2).split('.');
  
  // Indian numbering: first group of 3 from right, then groups of 2
  let formatted = '';
  let count = 0;
  
  for (let i = integerPart.length - 1; i >= 0; i--) {
    if (count === 3 || (count > 3 && (count - 3) % 2 === 0)) {
      formatted = ',' + formatted;
    }
    formatted = integerPart[i] + formatted;
    count++;
  }
  
  return decimalPart ? `${formatted}.${decimalPart}` : formatted;
}

/**
 * Format currency in INR with symbol
 * Example: 1234567 → ₹12,34,567.00
 */
export function formatCurrency(amount, showDecimals = true) {
  if (!amount && amount !== 0) return `${CURRENCY_SYMBOL}0.00`;
  
  const formatted = formatIndianNumber(amount);
  
  if (showDecimals) {
    const [int, dec] = formatted.split('.');
    return `${CURRENCY_SYMBOL}${int}.${dec || '00'}`;
  }
  
  return `${CURRENCY_SYMBOL}${formatted.split('.')[0]}`;
}

/**
 * Convert to words (Indian system: Lakhs, Crores)
 * Example: 150000 → "1.5 Lakhs"
 */
export function formatInWords(amount) {
  const num = parseFloat(amount);
  
  if (num >= 10000000) { // 1 crore
    return `${(num / 10000000).toFixed(2)} Cr`;
  } else if (num >= 100000) { // 1 lakh
    return `${(num / 100000).toFixed(2)} L`;
  } else if (num >= 1000) { // 1 thousand
    return `${(num / 1000).toFixed(2)} K`;
  }
  
  return num.toFixed(2);
}

/**
 * Parse Indian formatted number to float
 * Example: "12,34,567.00" → 1234567.00
 */
export function parseIndianNumber(str) {
  if (typeof str === 'number') return str;
  return parseFloat(str.replace(/,/g, ''));
}

/**
 * Get currency input props for forms
 */
export function getCurrencyInputProps() {
  return {
    prefix: CURRENCY_SYMBOL,
    placeholder: '0.00',
    step: '0.01',
    min: '0'
  };
}
