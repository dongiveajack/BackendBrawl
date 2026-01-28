import http from 'k6/http';
import { check } from 'k6';
import { Trend, Counter } from 'k6/metrics';

const goTrend = new Trend('go_duration');
const javaTrend = new Trend('java_duration');
const pythonTrend = new Trend('python_duration');

const goReqs = new Counter('go_reqs');
const javaReqs = new Counter('java_reqs');
const pythonReqs = new Counter('python_reqs');

export const options = {
    summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
    //discardResponseBodies: true,
    scenarios: {
        // go_test: {
        //     executor: 'ramping-vus',
        //     startVUs: 0,
        //     stages: [
        //         { duration: '20s', target: 1000 },
        //         { duration: '40s', target: 2000 },
        //         { duration: '5s', target: 0 },
        //     ],
        //     gracefulStop: '5s',
        //     exec: 'goRequest',
        // },
        java_test: {
            executor: 'ramping-vus',
            startVUs: 300,
            stages: [
                { duration: '30s', target: 1000 },
                { duration: '60s', target: 2000 },
                { duration: '10s', target: 0 },
            ],
            gracefulStop: '10s',
            startTime: '0s',
            exec: 'javaRequest',
        },
        // python_test: {
        //     executor: 'ramping-vus',
        //     startVUs: 0,
        //     stages: [
        //         { duration: '20s', target: 1000 },
        //         { duration: '40s', target: 2000 },
        //         { duration: '5s', target: 0 },
        //     ],
        //     gracefulStop: '5s',
        //     startTime: '80s',
        //     exec: 'pythonRequest',
        // },
    },
};

export function goRequest() {
    const res = http.get('http://127.0.0.1:8080/cache');
    check(res, { 'status is 200': (r) => r.status === 200 });
    goTrend.add(res.timings.duration);
    goReqs.add(1);
}

export function javaRequest() {
    const res = http.get('http://127.0.0.1:8081/cache');
    check(res, { 'status is 200': (r) => r.status === 200 });
    javaTrend.add(res.timings.duration);
    javaReqs.add(1);
}

export function pythonRequest() {
    const res = http.get('http://127.0.0.1:8082/cache');
    check(res, { 'status is 200': (r) => r.status === 200 });
    pythonTrend.add(res.timings.duration);
    pythonReqs.add(1);
}
