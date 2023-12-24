import { getUnit } from "../calc/unit.js";
const getDay = getUnit["d" /* Unit.day */];
const dd = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
const thMap = ["th", "st", "nd", "rd"];
const thFn = (num) => num + (thMap[num] || (num > 20 && thMap[num % 10]) || thMap[0]);
const getTime = getUnit["T" /* Unit.time */];
export const formatHandlers = {
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
