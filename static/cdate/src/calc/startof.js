import { add } from "./add.js";
import { getShortUnit, unitMS } from "./unit.js";
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
export const startOf = (dt, unit) => {
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
