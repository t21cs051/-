import { formatPlugin } from "./format/texter.js";
import { calcPlugin } from "./calc/calc.js";
import { adjustDateLike, tzPlugin } from "./timezone/timezone.js";
import { DateUTC } from "./timezone/dateutc.js";
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
export const cdate = new CDateCore(0, null)
    .plugin(formatPlugin)
    .plugin(calcPlugin)
    .plugin(tzPlugin)
    .cdateFn();
