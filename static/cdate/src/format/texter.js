import { en_US } from "./en_US.js";
import { strftimeHandlers } from "./strftime.js";
import { formatHandlers } from "./format.js";
import { localeHandlers } from "./locale.js";
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
export const texter = makeTexter().handler(baseHandlers).handler(en_US).handler(formatHandlers).handler(strftimeHandlers());
const _strftime = texter.strftime;
export const strftime = (fmt, dt) => _strftime(fmt, dt || new Date());
const getTexter = (x) => (x && x.tx || texter);
export const formatPlugin = (Parent) => {
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
