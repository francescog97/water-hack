import {defineConfig} from '@playwright/test';
export default defineConfig({
 testDir:'./tests/e2e',fullyParallel:false,workers:1,timeout:45000,
 expect:{timeout:10000},reporter:[['list'],['json',{outputFile:'test-results/results.json'}]],
 use:{baseURL:process.env.C2A_TEST_BASE_URL??'http://127.0.0.1:8000',browserName:'chromium',channel:'msedge',headless:true,viewport:{width:1366,height:900},trace:'retain-on-failure',screenshot:'only-on-failure'},
 webServer:process.env.C2A_TEST_BASE_URL?undefined:{command:'.venv/Scripts/python.exe -m uvicorn app.backend.app.main:app --host 127.0.0.1 --port 8000',url:'http://127.0.0.1:8000/api/health',reuseExistingServer:true,timeout:30000},
});
