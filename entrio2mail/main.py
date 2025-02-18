import time
import sys
import schedule
from playwright.sync_api import sync_playwright
from poschtar.main import gmail_end_user_credentials, get_sender_mail_and_display_name, gmail_compose, gmail_send

try:
    from credentials import *
except:
    sys.path.append("/root/.config/entrio2mail")
    from credentials import *

def login(page):
    print("[ENTR]: login")
    page.goto(ENTRIO_WEB_PAGE)
    page.get_by_role("button", name="Prihvati sve").click()
    page.get_by_role("textbox", name="E-mail", exact=True).click()
    page.get_by_role("textbox", name="E-mail", exact=True).fill(ENTRIO_USERNAME)
    page.get_by_role("textbox", name="Lozinka").click()
    page.get_by_role("textbox", name="Lozinka").fill(ENTRIO_PASSWORD)
    page.get_by_role("button", name="Prijavi se", exact=True).click()
    page.get_by_role("button", name="Ne hvala").click()
    page.locator("span[type='']").text_content
    page.wait_for_selector("span.big-magenta", state="visible", timeout=5000)

def get_sold_tickets_count(page):
    pl = page.locator("span.big-magenta")
    sold_tickets_count = int(pl.all_text_contents()[0])
    print(f"[ENTR]: sold_tickets_count = {sold_tickets_count}")
    return sold_tickets_count

def get_statistics_attachment(page):
    page.get_by_role("link", name="Statistika i izvještaji").click()
    page.get_by_role("button", name="Generiraj izvještaj po danima").click()
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Generiraj izvješće").click()
    print(f"[ENTR]: attachment = {download_info.value.suggested_filename}")
    filename = f"/tmp/{download_info.value.suggested_filename}"
    download_info.value.save_as(filename)
    return filename

def get_entrio_data():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()

        try:
            page = context.new_page()

            login(page)
            sold_tickets_count = get_sold_tickets_count(page)
            attachment = get_statistics_attachment(page)

            #import nest_asyncio
            #nest_asyncio.apply()
            #from IPython import embed; embed()

            return sold_tickets_count, attachment
        except Exception as e:
            print(f"[ENTR]: Error getting entrio data: {e}")
            sys.exit(1)

        finally:
            context.close()
            browser.close()

def send_mail(mail, subject, body, attachments):
    creds = gmail_end_user_credentials() 
    sender_mail, sender_display_name = get_sender_mail_and_display_name(creds)
    print(f"[SM]: {mail}")
    mail_content = gmail_compose(sender_mail, sender_display_name, subject, mail, body, attachments)
    gmail_send(creds, mail_content)

def generate_mail(production = False):
    print(f"[RUN]: production = {production}")
    sold_tickets_count, attachment = get_entrio_data()
    subject = "Entrio statistics for Postmodern Jukebox (PMJ)"
    body = f"Total sold tickets: {sold_tickets_count}.\nPlease do not reply to this automated message."
    if TEST: production = False
    if production:
        send_mail(MAIL_RECIPIENTS_PRODUCTION, subject, body, [attachment])
    else:
        send_mail(MAIL_RECIPIENTS_TEST, subject, body, [attachment])

def run():
    schedule.every().day.at("17:00").do(lambda: generate_mail(production = True) if time.localtime().tm_wday == 1 else generate_mail(production = False))
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run()
    #generate_mail(False)
