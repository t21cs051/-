import { getShortUnit, unitMS } from "./unit.js";
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
export const add = (dt, diff, unit) => {
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
