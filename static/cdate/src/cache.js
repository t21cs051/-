/**
 * cache
 */
export const cached = (fn) => {
    let cached = {};
    return key => (cached[key] || (cached[key] = fn(key)));
};
