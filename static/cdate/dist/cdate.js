'use strict';

const weekdayShort = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const weekdayLong = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const monthShort = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const monthLong = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const en_US = {
    // "%a": the locale's abbreviated weekday name
    "%a": dt => weekdayShort[dt.getDay()],
    // "%A": the locale's full weekday name
    "%A": dt => weekdayLong[dt.getDay()],
    // "%b": the locale's abbreviated month name
    "%b": dt => monthShort[dt.getMonth()],
    // "%B": the locale's full month name
    "%B": dt => monthLong[dt.getMonth()],
    // "%p": the locale's equivalent of either `AM` or `PM`
    "%p": dt => (dt.getHours() < 12 ? "AM" : "PM"),
    // "%r": the locale's representation of 12-hour clock time using AM/PM notation
    // 3:04:05 AM
    "%r": "%-I:%M:%S %p",
    // "%x": the locale's appropriate date representation
    // 1/2/22
    "%x": "%-m/%-d/%y",
    // "%X": the locale's appropriate time representation
    // 3:04:05 AM
    "%X": "%-I:%M:%S %p",
};

const unitMap = {
    year: "y" /* Unit.year */,
    month: "M" /* Unit.month */,
    week: "w" /* Unit.week */,
    date: "D" /* Unit.date */,
    day: "d" /* Unit.day */,
    hour: "h" /* Unit.hour */,
    minute: "m" /* Unit.minute */,
    second: "s" /* Unit.second */,
    millisecond: "ms" /* Unit.millisecond */,
};
Object.keys(unitMap).forEach((key) => {
    const s = (key + "s");
    const v = unitMap[key];
    if (v)
        unitMap[s] = unitMap[v] = v;
});
const getShortUnit = (unit) => {
    return unitMap[(unit || "ms" /* Unit.millisecond */)] ||
        unitMap[String(unit).toLowerCase()];
};
const unitMS = {
    h: 3600000 /* d.HOUR */,
    m: 60000 /* d.MINUTE */,
    s: 1000 /* d.SECOND */,
    ms: 1,
};
const getUnit = {
    y: dt => dt.getFullYear(),
    M: dt => dt.getMonth(),
    D: dt => dt.getDate(),
    d: dt => dt.getDay(),
    h: dt => dt.getHours(),
    m: dt => dt.getMinutes(),
    s: dt => dt.getSeconds(),
    ms: dt => dt.getMilliseconds(),
    TZO: dt => dt.getTimezoneOffset(),
    T: dt => dt.getTime(),
};

const strftimeHandlers = () => {
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

const getDay = getUnit["d" /* Unit.day */];
const dd = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
const thMap = ["th", "st", "nd", "rd"];
const thFn = (num) => num + (thMap[num] || (num > 20 && thMap[num % 10]) || thMap[0]);
const getTime = getUnit["T" /* Unit.time */];
const formatHandlers = {
    YY: "%y",
    YYYY: "%Y",
    M: "%-m",
    MM: "%m",
    MMM: "%b",
    MMMM: "%B",
    D: "%-d",
    Do: dt => thFn(dt.getDate()),
    DD: "%d",
    d: "%w",
    dd: dt => dd[getDay(dt)],
    ddd: "%a",
    dddd: "%A",
    H: "%-H",
    HH: "%H",
    h: "%-I",
    hh: "%I",
    m: "%-M",
    mm: "%M",
    s: "%-S",
    ss: "%S",
    SSS: "%L",
    Z: "%:z",
    ZZ: "%z",
    A: "%p",
    a: "%P",
    X: "%s",
    x: getTime, // Unix Millisecond Timestamp
};

/**
 * cache
 */
const cached = (fn) => {
    let cached = {};
    return key => (cached[key] || (cached[key] = fn(key)));
};

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
const getLocaleOptions = () => {
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
const localeHandlers = cached(makeLocale);

const mergeRouter = (a, b) => ((a && b) ? ((specifier) => (a(specifier) || b(specifier))) : (a || b));
const makeRouter = (handlers) => (handlers && (specifier => handlers[specifier]));
// @see https://docs.ruby-lang.org/en/3.1/DateTime.html#method-i-strftime
const strftimeRE = /%(?:[EO]\w|[0_#^-]?[1-9]?\w|::?z|[%+])/g;
// /\[(.*?)\]|A+|a+|B+|b+|C+|c+|...|Z+|z+/g
const makeFormatRE = () => {
    let re = ["\\[(.*?)\\]", "[A-Za-z]o"];
    const c = (code) => String.fromCharCode(code + 65) + "+";
    for (let i = 0; i < 26; i++) {
        re.push(c(i), c(i + 32));
    }
    return new RegExp(re.join("|"), "g");
};
const formatRE = makeFormatRE();
const baseHandlers = {
    // default specifiers for .text() .strftime() with milliseconds
    ISO: "%Y-%m-%dT%H:%M:%S.%L%:z",
    // default specifiers for .format() without milliseconds
    undef: "YYYY-MM-DDTHH:mm:ssZ",
    // Invalid Date
    NaN: (new Date(NaN) + ""),
};
const makeTexter = (router) => {
    const one = (specifier, dt) => {
        let handler = router(specifier);
        if ("string" === typeof handler) {
            const next = router(handler);
            if (next != null)
                handler = next; // bypass strftime call
        }
        if ("function" === typeof handler) {
            return handler(dt);
        }
        else if (handler == null) {
            return specifier; // Unsupported specifiers
        }
        else {
            return strftime(handler, dt); // recursive call
        }
    };
    const out = {};
    const strftime = (fmt, dt) => {
        return fmt.replace(strftimeRE, (specifier) => one(specifier, dt));
    };
    out.strftime = (fmt, dt) => {
        if (isNaN(+dt))
            return one("NaN", dt);
        if (fmt == null)
            return one("ISO", dt);
        return strftime(fmt, dt);
    };
    out.format = (fmt, dt) => {
        if (isNaN(+dt))
            return one("NaN", dt);
        if (fmt == null)
            fmt = String(router("undef"));
        return fmt.replace(formatRE, (specifier, raw) => (raw || one(specifier, dt)));
    };
    out.handler = specifiers => makeTexter(mergeRouter(makeRouter(specifiers), router));
    return out;
};
const texter = makeTexter().handler(baseHandlers).handler(en_US).handler(formatHandlers).handler(strftimeHandlers());
const _strftime = texter.strftime;
const strftime = (fmt, dt) => _strftime(fmt, dt || new Date());
const getTexter = (x) => (x && x.tx || texter);
const formatPlugin = (Parent) => {
    return class CDateFormat extends Parent {
        /**
         * updates strftime option with the given locale
         */
        handler(handlers) {
            const out = this.inherit();
            const { x } = out;
            x.tx = getTexter(x).handler(handlers);
            return out;
        }
        /**
         * returns a text with "YYYY-MM-DD" formatting style
         */
        format(fmt) {
            return getTexter(this.x).format(fmt, this.ro());
        }
        /**
         * returns a text with "%y/%m/%d formatting style
         */
        text(fmt) {
            return getTexter(this.x).strftime(fmt, this.ro());
        }
        locale(lang) {
            return this.handler(localeHandlers(lang));
        }
    };
};

const addMonth = (dt, months) => {
    const year = dt.getFullYear();
    const month = dt.getMonth();
    const date = dt.getDate();
    // calculate days between the months
    const tmp = new Date(year, month, 1);
    const before = +tmp;
    const diff = year * 12 + month + months;
    tmp.setFullYear(Math.floor(diff / 12));
    const newMonth = diff % 12;
    tmp.setMonth(newMonth);
    const days = Math.round((+tmp - before) / 86400000 /* d.DAY */);
    // move days
    addDay(dt, days);
    // check an overflow
    const newDate = dt.getDate();
    if (newMonth !== dt.getMonth() && date > newDate) {
        // the very last day of the previous month
        addDay(dt, -newDate);
    }
};
const addDay = (dt, days) => {
    const tz1 = dt.getTimezoneOffset();
    dt.setTime(+dt + days * 86400000 /* d.DAY */);
    const tz2 = dt.getTimezoneOffset();
    // adjustment for Daylight Saving Time (DST)
    if (tz1 !== tz2) {
        dt.setTime(+dt + (tz2 - tz1) * 60000 /* d.MINUTE */);
    }
};
const add = (dt, diff, unit) => {
    if (!diff)
        return;
    const u = getShortUnit(unit);
    const msec = unitMS[u];
    if (msec) {
        dt.setTime(+dt + diff * msec);
        return;
    }
    switch (u) {
        case "y" /* Unit.year */:
            return addMonth(dt, diff * 12);
        case "M" /* Unit.month */:
            return addMonth(dt, diff);
        case "w" /* Unit.week */:
            return addDay(dt, diff * 7);
        case "D" /* Unit.date */:
        case "d" /* Unit.day */:
            return addDay(dt, diff);
    }
};

const startOfMonth = (dt) => {
    startOfDay(dt);
    add(dt, 1 - dt.getDate(), "day");
};
const startOfDay = (dt) => {
    const tz1 = dt.getTimezoneOffset();
    truncate(dt, 86400000 /* d.DAY */);
    const tz2 = dt.getTimezoneOffset();
    // adjustment for Daylight Saving Time (DST)
    if (tz1 !== tz2) {
        dt.setTime(+dt + (tz2 - tz1) * 60000 /* d.MINUTE */);
    }
};
const truncate = (dt, unit) => {
    const tz = dt.getTimezoneOffset() * 60000 /* d.MINUTE */;
    dt.setTime(Math.floor((+dt - tz) / unit) * unit + tz);
};
const startOf = (dt, unit) => {
    const u = getShortUnit(unit);
    const msec = unitMS[u];
    if (msec)
        return truncate(dt, msec);
    switch (u) {
        case "y" /* Unit.year */:
            startOfMonth(dt);
            return add(dt, -dt.getMonth(), "M" /* Unit.month */);
        case "M" /* Unit.month */:
            return startOfMonth(dt);
        case "w" /* Unit.week */:
            startOfDay(dt);
            return add(dt, -dt.getDay(), "d" /* Unit.day */);
        case "D" /* Unit.date */:
        case "d" /* Unit.day */:
            return startOfDay(dt);
    }
};

const calcPlugin = (Parent) => {
    return class CDateCalc extends Parent {
        /**
         * getter
         */
        get(unit) {
            const fn = getUnit[getShortUnit(unit)];
            if (fn)
                return fn(this.ro());
        }
        /**
         * setter
         */
        set(unit, value) {
            unit = getShortUnit(unit);
            const fn = getUnit[unit];
            if (!fn)
                return this;
            const dt = this.rw();
            add(dt, (value - fn(dt)), unit);
            return this.create(dt);
        }
        /**
         * returns a new CDate object manipulated
         */
        startOf(unit) {
            unit = getShortUnit(unit);
            if (!unit)
                return this;
            const dt = this.rw();
            startOf(dt, unit);
            return this.create(dt);
        }
        /**
         * returns a new CDate object manipulated
         */
        endOf(unit) {
            unit = getShortUnit(unit);
            if (!unit)
                return this;
            const dt = this.rw();
            startOf(dt, unit);
            add(dt, 1, unit);
            add(dt, -1);
            return this.create(dt);
        }
        /**
         * returns a new CDate object manipulated
         */
        add(diff, unit) {
            unit = getShortUnit(unit);
            if (!unit)
                return this;
            const dt = this.rw();
            add(dt, diff, unit);
            return this.create(dt);
        }
        /**
         * returns a new CDate object manipulated
         */
        next(unit) {
            return this.add(1, unit);
        }
        /**
         * returns a new CDate object manipulated
         */
        prev(unit) {
            return this.add(-1, unit);
        }
    };
};

const shorten = (s) => String(s).toLowerCase().substr(0, 2);
const weekdayMap = { su: 0, mo: 1, tu: 2, we: 3, th: 4, fr: 5, sa: 6 };
const calcTimeZoneOffset = (dtf, dt) => {
    const parts = dtf.formatToParts(dt);
    const index = {};
    parts.forEach(v => (index[v.type] = v.value));
    // difference of days:
    const wday = weekdayMap[shorten(index.weekday)];
    let day = (7 + dt.getUTCDay() - wday) % 7;
    if (day > 3)
        day -= 7;
    // difference of hours: some locales use h24
    const hour = dt.getUTCHours() - (index.hour % 24);
    // difference of minutes:
    const minutes = dt.getUTCMinutes() - index.minute;
    // difference of seconds:
    const seconds = dt.getUTCSeconds() - index.second;
    // difference in minutes:
    return -((day * 24 + hour) * 60 + minutes + (seconds / 60));
};
const getTZF = cached(tz => {
    // cache latest results
    let cache = {};
    let count = 0;
    let dtf;
    return ms => {
        // time zone offset never changes within every 15 minutes
        const minute15 = Math.floor(ms / 900000 /* d.MINUTE15 */);
        // check cached result
        let offset = cache && cache[minute15];
        if (offset != null)
            return offset;
        // reset all cache simply at every 24 x 4 times
        if (count++ > 96) {
            cache = {};
            count = 0;
        }
        const dt = new Date(ms);
        // DateTimeFormat is much slow
        if (!dtf) {
            const numeric = "numeric";
            dtf = new Intl.DateTimeFormat("en-US", { timeZone: tz, hour12: false, weekday: "short", hour: numeric, minute: numeric, second: numeric });
        }
        offset = calcTimeZoneOffset(dtf, dt);
        // fallback to local time zone
        if (offset == null) {
            offset = -dt.getTimezoneOffset();
        }
        // write to cache
        cache[minute15] = offset;
        return offset;
    };
});

class DateUTC {
    constructor(t) {
        this.dt = new Date(t);
    }
    valueOf() {
        return +this.dt;
    }
    setTime(msec) {
        return this.dt.setTime(msec);
    }
    getTimezoneOffset() {
        return 0; // always UTC
    }
    getMilliseconds() {
        return this.dt.getUTCMilliseconds();
    }
    getSeconds() {
        return this.dt.getUTCSeconds();
    }
    getMinutes() {
        return this.dt.getUTCMinutes();
    }
    getHours() {
        return this.dt.getUTCHours();
    }
    getDay() {
        return this.dt.getUTCDay();
    }
    getDate() {
        return this.dt.getUTCDate();
    }
    ;
    getMonth() {
        return this.dt.getUTCMonth();
    }
    getFullYear() {
        return this.dt.getUTCFullYear();
    }
    getTime() {
        return +this;
    }
}

class DateTZ extends DateUTC {
    constructor(t, tzf) {
        const tzo = tzf(t);
        super(t + tzo * 60000 /* d.MINUTE */);
        this.t = t;
        this.tzf = tzf;
        this.tzo = tzo;
    }
    valueOf() {
        return this.t;
    }
    setTime(msec) {
        const tzo = this.tzo = this.tzf(msec);
        this.dt.setTime(+msec + tzo * 60000 /* d.MINUTE */);
        return this.t = msec;
    }
    getTimezoneOffset() {
        return -this.tzo;
    }
}
const tzPlugin = (Parent) => {
    return class CDateTZ extends Parent {
        utc(keepLocalTime) {
            const out = this.inherit();
            out.x.rw = (dt) => new DateUTC(+dt);
            if (keepLocalTime)
                return adjustTimeZoneOffset(this, out);
            return out;
        }
        /**
         * "+0900", "+09:00", "GMT+09:00", "Z", "UTC",...
         */
        utcOffset(offset, keepLocalTime) {
            if (offset == null) {
                return 0 - getTimezoneOffset(this.ro());
            }
            const out = this.inherit();
            out.x.rw = (dt) => new DateTZ(+dt, parseTZ(offset));
            if (keepLocalTime)
                return adjustTimeZoneOffset(this, out);
            return out;
        }
        /**
         * "Asia/Tokyo", "America/New_York",...
         */
        tz(timeZoneName, keepLocalTime) {
            const out = this.inherit();
            out.x.rw = (dt) => new DateTZ(+dt, getTZF(timeZoneName));
            if (keepLocalTime)
                return adjustTimeZoneOffset(this, out, true);
            return out;
        }
    };
};
const adjustTimeZoneOffset = (before, after, hasDST) => {
    const dt1 = before.ro();
    const dt2 = after.rw();
    adjustDateLike(dt1, dt2, hasDST);
    return after.create(dt2);
};
const adjustDateLike = (before, after, hasDST) => {
    const tz1 = getTimezoneOffset(before);
    const tz2 = getTimezoneOffset(after);
    if (tz1 === tz2)
        return;
    add(after, tz2 - tz1, "m" /* Unit.minute */);
    if (!hasDST)
        return;
    const tz3 = getTimezoneOffset(after);
    if (tz2 === tz3)
        return;
    // adjustment for Daylight Saving Time (DST)
    add(after, tz3 - tz2, "m" /* Unit.minute */);
};
const getTimezoneOffset = getUnit.TZO;
const parseTZ = cached((offset) => {
    if ("number" === typeof offset) {
        if (-16 < offset && offset < 16) {
            offset *= 60;
        }
    }
    else {
        const matched = String(offset).match(/(?:^|GMT)?(?:([+-])([01]?\d):?(\d[05])|$)|(UTC|Z)$/);
        if (!matched)
            return;
        offset = ((+matched[2]) * 60 + (+matched[3])) | 0;
        if (matched[1] === "-")
            offset = 0 - offset;
    }
    return (_) => offset;
});

class CDateCore {
    /**
     * the constructor
     */
    constructor(t, x) {
        this.t = t;
        if ("number" !== typeof t) {
            this.d = t;
        }
        this.x = x || Object.create({ cdate: {} });
    }
    /**
     * cdate function factory
     */
    cdateFn() {
        return cdateFn(this);
    }
    /**
     * returns a read-write version of DateLike for manipulation
     */
    rw() {
        const t = +this.t;
        const rw = this.x.rw;
        return rw ? rw(t) : new Date(t);
    }
    /**
     * returns a read-only version of DateLike for displaying
     */
    ro() {
        return this.d || (this.d = this.rw());
    }
    /**
     * returns milliseconds since the epoch
     */
    valueOf() {
        return +this.ro();
    }
    /**
     * returns a bare Date object
     */
    toDate() {
        return new Date(+this);
    }
    /**
     * returns a JSON representation of Date
     */
    toJSON() {
        return this.toDate().toJSON();
    }
    /**
     * returns an instance including the plugin
     */
    plugin(fn) {
        const CDateClass = this.constructor;
        const CDateX = fn(CDateClass) || CDateClass;
        return new CDateX(this.t, this.x);
    }
    /**
     * creates another CDate object with the DateLike given
     */
    create(dt) {
        return new this.constructor(dt, this.x);
    }
    /**
     * clones the CDate object
     */
    inherit() {
        const out = this.create(+this);
        // x is readonly
        out.x = Object.create(out.x);
        return out;
    }
}
const cdateFn = (base) => {
    return (dt) => {
        if (dt == null) {
            dt = new Date(); // now
        }
        else if ("string" === typeof dt) {
            dt = +parseDate(dt, base.x.rw);
        }
        return base.create(+dt);
    };
};
const parseDate = (dt, rwFn) => {
    const matched = 
    // ISO 8601
    dt.match(/^(\d{4}|[-+]\d{4,6})(?:(-)(\d{2})(?:-(\d{2})(?:T((\d{2}):(\d{2})(?::(\d{2})(\.\d+)?)?))?)?)?$/) ||
        // Loose format
        dt.match(/^(\d{4}|[-+]\d{4,6})(?:([-/])(\d+)(?:\2(\d+)(?:\s+((\d+):(\d+)(?::(\d+)(\.\d+)?)?))?)?)?$/);
    if (!matched) {
        return new Date(dt); // native parser
    }
    // ISO 8601 parser
    const year = +matched[1] || 0;
    const month = +matched[3] - 1 || 0;
    const date = +matched[4] || 1;
    const hour = +matched[6] || 0;
    const minute = +matched[7] || 0;
    const second = +matched[8] || 0;
    const ms = (+matched[9]) * 1000 || 0;
    const yoffset = (0 <= year && year < 100) ? 100 : 0;
    if (rwFn) {
        // UTC
        const tmp = new Date(Date.UTC(year + yoffset, month, date, hour, minute, second, ms));
        if (yoffset)
            tmp.setUTCFullYear(year);
        const dt1 = new DateUTC(+tmp); // DateUTC only
        const dt2 = rwFn(+tmp); // DateUTC or DateTZ
        adjustDateLike(dt1, dt2, true);
        return dt2;
    }
    else {
        // local time
        const dt = new Date(year + yoffset, month, date, hour, minute, second, ms);
        if (yoffset)
            dt.setFullYear(year);
        return dt;
    }
};
const cdate = new CDateCore(0, null)
    .plugin(formatPlugin)
    .plugin(calcPlugin)
    .plugin(tzPlugin)
    .cdateFn();

exports.cdate = cdate;
exports.strftime = strftime;
