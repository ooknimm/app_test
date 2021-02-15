const puppeteer = require('puppeteer');

(async () => {
        const browser = await puppeteer.launch({
            headless : false,
            defaultViewport : null
        });

        const page = await browser.newPage();
        await page.goto('https://apptest.ai/');
        await page.waitFor(1000);
        
        // 메뉴 클릭 로직
        // 상단 메뉴의 a 태그를 배열에 저장
        let menuElement = await page.$$('#menu-standard > li > a');

        for (let i = 0; i < menuElement.length-1; i++) {
            await menuElement[i].click();
            await page.waitFor(1000);
            // 페이지가 바뀌기 때문에 요소를 다시 탐색
            menuElement = await page.$$('#menu-standard > li > a');
            // 중간에 메뉴 탭이 없는 페이지가 존재하기 때문에 사용
            if (menuElement.length == 0) {
                await page.goBack();
                menuElement = await page.$$('#menu-standard > li > a');
            }
        }

        // 메시지 보내기 로직
        // 메시지란의 form, input, textarea 태그를 배열에 저장
        let inputElement = await page.$$('#wpcf7-f1216-p1183-o2 > form input, textarea');
        for (let element of inputElement) {
            // class 이름을 가져와 변수에 할당
            let value = await (await element.getProperty('className')).jsonValue();
            
            if (value == '') {
                continue
            // 버튼인 경우 클릭
            } else if (await value.includes('submit')) {
                await element.click();
                await page.waitFor(1000);
                break
            // 이메일인 경우 이메일로 입력
            } else if (await value.includes('email')) {
                await element.focus();
                await element.type('hello@naver.com');
            // 나머지는 같은 텍스트를 입력
            } else {
                await element.focus();
                await element.type('hi');
                await page.waitFor(1000);
            }
        }
        await page.waitFor(2000);
        await browser.close();
    }
)();