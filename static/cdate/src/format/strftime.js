import { getUnit } from "../calc/unit.js";
export const strftimeHandlers = () => {
    const pad2 = fn => (dt) => ("0" + fn(dt)).substr(-2);
    const pad2S = fn => (dt) => (" " + fn(dt)).substr(-2);
    const pad3 = fn => (dt) => ("00" + fn(dt)).substr(-3);
    const padY = fn => (dt) => {
        let year = fn(dt);
        if (0 <= year && year <= 9999) {
            return ("000" + year).substr(-4);
        }
        let prefix = "+";
        if (year < 0) {
            prefix = "-";
            year = -year;
        }
        return prefix + (("00000" + year).substr(-6));
    };
    const getFullYear = getUnit["y" /* Unit.year */];
    const getMonth = getUnit["M" /* Unit.month */];
    const getDate = getUnit["D" /* Unit.date */];
    const getDay = getUnit["d" /* Unit.day */];
    const getHours = getUnit["h" /* Unit.hour */];
    const getMinutes = getUnit["m" /* Unit.minute */];
    const getSeconds = getUnit["s" /* Unit.second */];
    const getMilliseconds = getUnit["ms" /* Unit.millisecond */];
    const getTime = getUnit["T" /* Unit.time */];
    const getTimezoneOffset = getUnit["TZO" /* Unit.timeZoneOffset */];
    const C = dt => Math.floor(getFullYear(dt) / 100);
    const I = dt => (((getHours(dt) + 11) % 12) + 1);
    const m = dt => (getMonth(dt) + 1);
    const y = dt => (getFullYear(dt) % 100);
    const pad0 = (num) => (num < 10 ? "0" + num : num);
    const makeZ = (delim, hasSecond) => {
        return dt => {
            let offset = -getTimezoneOffset(dt);
            const isMinus = (offset < 0);
            if (isMinus)
                offset = -offset;
            const hour = Math.floor(offset / 60);
            const min = Math.floor(offset % 60);
            const second = hasSecond ? delim + pad0(Math.floor((offset % 1) * 60)) : "";
            return (isMinus ? "-" : "+") + pad0(hour) + delim + pad0(min) + second;
        };
    };
    /**
     * %c %r %x and %X are defined at locale files
     */
    const handlers = {
        // "%c": the locale's appropriate date and time representation
        "%c": "%a %b %e %T %Y",
        // "%C": the century as a decimal number
        "%-C": C,
        "%C": pad2(C),
        // "%d": the day of the month as a decimal number
        "%-d": getDate,
        "%d": pad2(getDate),
        // "%D": the date in the format `%m/%d/%y`
        "%D": "%m/%d/%y",
        // "%e": the day of month as a decimal number
        "%e": pad2S(getDate),
        // "%F": the date in the format `%Y-%m-%d`
        "%F": "%Y-%m-%d",
        // "%H": the hour (24-hour clock) as a decimal number
        "%-H": getHours,
        "%H": pad2(getHours),
        // "%I": the hour (12-hour clock) as a decimal number
        "%-I": I,
        "%I": pad2(I),
        // "%k": the hour (24-hour clock) as a decimal number
        "%k": pad2S(getHours),
        // "%l": the hour (12-hour clock) as a decimal number
        "%l": pad2S(I),
        // "%L": the millisecond as a decimal number
        "%-L": pad3(getMilliseconds),
        "%L": pad3(getMilliseconds),
        // "%m": the month as a decimal number
        "%-m": m,
        "%m": pad2(m),
        // "%M": the minute as a decimal number
        "%-M": getMinutes,
        "%M": pad2(getMinutes),
        "%P": dt => (getHours(dt) < 12 ? "am" : "pm"),
        // "%R": the time in the format `%H:%M`
        "%R": "%H:%M",
        // "%s": the number of seconds since the Epoch, UTC
        "%s": dt => Math.floor(getTime(dt) / 1000),
        // "%S": the second as a decimal number
        "%-S": getSeconds,
        "%S": pad2(getSeconds),
        // "%T": the time in the format `%H:%M:%S`
        "%T": "%H:%M:%S",
        // "%y": the year without century as a decimal number
        "%-y": y,
        "%y": pad2(y),
        // "%Y": the year with century as a decimal number
        "%-Y": getFullYear,
        "%Y": padY(getFullYear),
        // "%u": the weekday (Monday as the first day of the week) as a decimal number
        "%u": dt => ((getDay(dt) + 6) % 7 + 1),
        // "%v": the date in the format `%e-%b-%Y`
        "%v": "%e-%b-%Y",
        // "%w": the weekday (Sunday as the first day of the week) as a decimal number
        "%w": getDay,
        // "%z": the offset from UTC in the format `+HHMM` or `-HHMM`
        "%::z": makeZ(":", true),
        "%:z": makeZ(":"),
        "%z": makeZ(""),
        // "%%": a literal `%` character
        "%%": () => "%",
        // "%n": a newline character
        "%n": () => "\n",
        // "%t": a tab character
        "%t": () => "\t",
        // ==== NOT IMPLEMENTED HANDLERS BELOW ====
        // "%G": the ISO 8601 year with century as a decimal number
        // "%g": the ISO 8601 year without century as a decimal number
        // "%j": the day of the year as a decimal number
        // "%U": the week number of the year (Sunday as the first day of the week)
        // "%V": the week number of the year (Monday as the first day of the week)
        // "%W": the week number of the year (Monday as the first day of the week)
        // "%Z": the time zone name
    };
    const modificate = (c, specifier) => {
        specifier.split("").forEach(s => handlers[c + s] = handlers["%" + s]);
    };
    // Modified Conversion Specifiers
    modificate("%E", "cCxXyY");
    modificate("%O", "deHImMSuUVwWy");
    return handlers;
};
