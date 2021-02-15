const puppeteer = require('puppeteer');

(async () => {
        const browser = await puppeteer.launch({
            headless : false,
            defaultViewport : null
        });
        const page = await browser.newPage();
        await page.goto('https://apptest.ai/');
        await page.waitFor(1000);
        // a태그의 링크를 배열에 저장
        let linkElement = await page.$$eval('a', element => {
            return element.map(el => {
                return el.href;
            })
        });
        // 중복 요소 제거
        let elementList = Array.from(new Set(linkElement));
        // json파일로 저장
        const fs = require('fs');
        fs.writeFile('./scrapingJson.json', JSON.stringify(elementList), err => err ? console.log(err): null);
        await browser.close();
        //json 읽기 및 스크린샷 작업 수행
        await readJson();
    }
)();

async function readJson() {
    const browser = await puppeteer.launch({
        headless : false,
        defaultViewport : null
    });

    const page = await browser.newPage();
    await page.goto('https://apptest.ai/');
    await page.waitFor(1000);

    // json 파일을 읽음
    const fs = require('fs');
    let jsonElement = await JSON.parse(fs.readFileSync('./scrapingJson.json'));
    
    const pathFolder = './screenshots/'
    // 폴더가 존재하지 않으면 폴더 생성
    const makeFolder = (dir) => {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }
    }
    makeFolder(pathFolder);

    for (let i = 0; i < jsonElement.length; i++) {
        const href = `a[href="${jsonElement[i]}"]`;
        const element = await page.$(href);
        if (element !== null) {
            // _self를 지정해서 해당 탭에서 작업을 수행한다.
            await page.evaluateHandle((el) => {
                el.target = '_self';
         }, element)
            // 이메일링크는 무시 (지메일이 열리기 때문)
            if (href.includes('mailto')) {
                continue
            } else {
                await ele.click();
                //void 링크의 경우 waitForNavigation를 사용하면 타임아웃이 걸린다.
                if (!href.includes('javascript:void')) {
                    await page.waitForNavigation();
                }
                await page.waitFor(3000);
                await page.screenshot({path : `${pathFolder}/screenshot${i}.png`});
                await page.goto('https://apptest.ai/');
            }
        }
    }
    await browser.close();
};