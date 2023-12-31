import { getTZF } from "./tzf.js";
import { DateUTC } from "./dateutc.js";
import { cached } from "../cache.js";
import { getUnit } from "../calc/unit.js";
import { add } from "../calc/add.js";
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
export const tzPlugin = (Parent) => {
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
export const adjustDateLike = (before, after, hasDST) => {
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
