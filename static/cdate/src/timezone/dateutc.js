export class DateUTC {
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
