import { cached } from "../cache.js";
/**
 * build an on-demand Handlers for the language specified
 */
const makeLocale = (lang) => {
    // build a handler function which converts from Date to string
    const makeHandler = (options, keyFn, partType) => {
        let format;
        const handler = (dt) => {
            // force UTC instead of local time
            const offset = dt.getTimezoneOffset();
            const utc = new Date(+dt - offset * 60000 /* d.MINUTE */);
            // cached DateTimeFormat instance
            if (!format)
                format = new Intl.DateTimeFormat(lang, options);
            // pickup only the single part of parts
            if (partType) {
                const part = format.formatToParts(utc).find(v => v.type === partType);
                return part && part.value;
            }
            // stringify
            const text = format.format(utc);
            // remove "UTC" string for some cases given
            if (text)
                return text.replace(/\s+UTC$/, "");
        };
        // on-demand use only
        if (!keyFn)
            return handler;
        // cached results
        const cache = {};
        return dt => {
            const key = keyFn(dt);
            return cache[key] || (cache[key] = handler(dt));
        };
    };
    // keyFn
    const getDay = (dt) => dt.getDay();
    const getMonth = (dt) => dt.getMonth();
    // Handlers
    return {
        "%a": makeHandler(styleOptions.a, getDay),
        "%A": makeHandler(styleOptions.A, getDay),
        "%b": makeHandler(styleOptions.b, getMonth),
        "%B": makeHandler(styleOptions.B, getMonth),
        "%c": makeHandler(styleOptions.c),
        "%p": makeHandler(styleOptions.p, dt => dt.getHours(), "dayPeriod"),
        "%r": makeHandler(styleOptions.r),
        "%x": makeHandler(styleOptions.x),
        "%X": makeHandler(styleOptions.X),
    };
};
export const getLocaleOptions = () => {
    const digits = "2-digit";
    const medium = "medium";
    const numeric = "numeric";
    const short = "short";
    const long = "long";
    // Note: "timeZoneName" parameter is not allowed here!
    const options = {
        a: { weekday: short },
        A: { weekday: long },
        b: { month: short },
        B: { month: long },
        c: { weekday: short, year: numeric, month: short, day: numeric, hour: digits, minute: digits, second: digits },
        p: { hour: numeric, hour12: true },
        r: { timeStyle: medium, hour12: true },
        x: { dateStyle: short },
        X: { timeStyle: medium }, // hour12: default
    };
    // force UTC instead of local time
    Object.keys(options).forEach((key) => options[key].timeZone = "UTC");
    return options;
};
const styleOptions = getLocaleOptions();
export const localeHandlers = cached(makeLocale);
