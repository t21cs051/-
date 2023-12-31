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
export const getShortUnit = (unit) => {
    return unitMap[(unit || "ms" /* Unit.millisecond */)] ||
        unitMap[String(unit).toLowerCase()];
};
export const unitMS = {
    h: 3600000 /* d.HOUR */,
    m: 60000 /* d.MINUTE */,
    s: 1000 /* d.SECOND */,
    ms: 1,
};
export const getUnit = {
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
