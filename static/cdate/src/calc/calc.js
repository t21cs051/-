import { add } from "./add.js";
import { startOf } from "./startof.js";
import { getUnit, getShortUnit } from "./unit.js";
export const calcPlugin = (Parent) => {
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
