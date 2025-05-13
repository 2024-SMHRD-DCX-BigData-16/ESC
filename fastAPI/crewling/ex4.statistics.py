import os
import re
import time
import pandas as pd
from urllib.parse import unquote
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from selenium import webdriver as wb
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_job():
    gtr_ymd = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    csv_path = f'/result/keyword_{gtr_ymd}.csv'

    if not os.path.exists(csv_path):
        print(f" 파일이 존재하지 않습니다: {csv_path}")
        return

    df_keyword = pd.read_csv(csv_path)
    if 'issue_keyword' not in df_keyword.columns:
        print(f" 'issue_keyword' 컬럼이 없습니다.")
        return

    keywords = df_keyword['issue_keyword'].dropna().unique().tolist()
    print(f" 총 {len(keywords)}개의 키워드 수집 예정")

    all_results = []

    for keyword in keywords:
        print(f"\n▶ 키워드 수집 시작: {keyword}")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-data-dir=/tmp/selenium_profile_{time.time()}")

        driver = wb.Chrome(options=options)

        try:
            driver.get('https://www.kostat.go.kr/unifSearch/search.es')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_ts_search")))
            search_input = driver.find_element(By.ID, "input_ts_search")
            search_input.clear()
            search_input.send_keys(keyword)
            driver.find_element(By.ID, "btn_ts_search").click()

            # 통계표 더보기 클릭 (statDB 탭)
            driver.execute_script("go_more('statDB','01');")
            time.sleep(3)

            aTags = driver.find_elements(By.CSS_SELECTOR, 'a.gsbl_link')
            for a in aTags[:10]:
                href = a.get_attribute('href')
                title = a.text.strip()

                try:
                    grandparent = a.find_element(By.XPATH, '../../..')  # 혹은 적절히 상위 계층 조정
                    info = grandparent.find_element(By.CSS_SELECTOR, 'p.gsbl_info').text.strip()
                except:
                    info = ""


                match = re.search(r"generator_link\('(\d+)','(DT_[^']+)','','([^']+)", href or "")
                if match:
                    orgId, tblId, full_path_encoded = match.groups()
                    full_path = unquote(full_path_encoded)
                    parts = full_path.split(" > ")
                    range_path = " > ".join(parts[:-1]) if len(parts) > 1 else full_path
                    url = f"https://kosis.kr/statHtml/statHtml.do?orgId={orgId}&tblId={tblId}"

                    all_results.append({
                        "keyword": keyword,
                        "title": title,
                        "range": range_path,
                        "info": info, 
                        "url": url,
                        "created_at": datetime.now(),
                    })

        except Exception as e:
            print(f" 수집 실패: {e}")
        finally:
            driver.quit()

    if not all_results:
        print(" 수집된 결과가 없습니다.")
        return

    df_result = pd.DataFrame(all_results)
    print(df_result)

    load_dotenv('.env')
    DB_URL = os.getenv("DB_URL")
    if not DB_URL:
        print("❌ DB_URL 환경 변수가 없습니다.")
        return

    engine = create_engine(DB_URL)

    try:
        df_result.to_sql(name='tbl_statistics', con=engine, if_exists='append', index=False)
        print(f"\n✅ 총 {len(df_result)}건 DB 저장 완료")
    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")


if __name__ == "__main__":
    run_job()
