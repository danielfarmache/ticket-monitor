"""
Ticket Monitor for Entertix.ro - CLOUD VERSION
Monitors for Rapid vs Cluj match tickets

This version is optimized to run 24/7 on cloud servers like PythonAnywhere.
It sends EMAIL alerts instead of sound alerts (since cloud servers have no speakers).
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
CHECK_INTERVAL = 300  # Check every 5 minutes (300 seconds)
URL = "https://www.entertix.ro/evenimente?s=rapid+"

# Email Configuration
GMAIL_ADDRESS = "daniel.m.farmache@gmail.com"
GMAIL_APP_PASSWORD = "lils iipd xcrz bwlx"  # Replace with your Gmail App Password
RECIPIENT_EMAIL = "daniel.farmache@dmfcapital.ro"

def check_for_match():
    """
    Checks Entertix.ro for any match involving Rapid and Cluj
    Returns True if both teams are mentioned anywhere on the page
    """
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking Entertix.ro...")
        
        # Send request to the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            # Convert to lowercase for easier searching
            page_content = response.text.lower()
            
            # Look for both Rapid and Cluj anywhere on the page
            # This will catch variations like "CFR Cluj", "U Cluj", "Cluj-Napoca", etc.
            if ('rapid' in page_content and 'cluj' in page_content):
                return True
        
        print("    No match found yet...")
        return False
        
    except Exception as e:
        print(f"    Error checking website: {e}")
        return False

def send_email(alert_number=1):
    """
    Sends an email alert when tickets are found
    """
    try:
        print(f"    Sending email alert #{alert_number}...")
        
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = GMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        
        if alert_number == 1:
            msg['Subject'] = "🎉 RAPID vs CLUJ TICKETS AVAILABLE! 🎉"
        else:
            msg['Subject'] = f"⚠️ REMINDER #{alert_number}: RAPID vs CLUJ TICKETS STILL AVAILABLE!"
        
        # Email body
        body = f"""
{'=' * 60}
TICKETS ARE NOW AVAILABLE!
{'=' * 60}

Match: Rapid vs Cluj
Website: Entertix.ro
Direct Link: {URL}

🚨 GO TO THE WEBSITE NOW TO PURCHASE YOUR TICKETS! 🚨

This is automated alert #{alert_number} from your Cloud Ticket Monitor.
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 60}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail's SMTP server and send
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"    ✅ Email alert #{alert_number} sent successfully!")
        return True
        
    except Exception as e:
        print(f"    ❌ Failed to send email: {e}")
        return False

def main():
    """
    Main monitoring loop
    """
    print("=" * 60)
    print("CLOUD TICKET MONITOR - Entertix.ro")
    print("Monitoring for: Rapid vs Cluj")
    print(f"Check interval: Every {CHECK_INTERVAL//60} minutes")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\n📧 Alerts will be sent via EMAIL to:", RECIPIENT_EMAIL)
    print("\nMonitoring started... (Press Ctrl+C to stop)\n")
    
    try:
        while True:
            # Check for the match
            if check_for_match():
                print("\n" + "!" * 60)
                print("🎉 TICKETS FOUND! 🎉")
                print("Rapid vs Cluj match is now on Entertix.ro!")
                print(f"Visit: {URL}")
                print("!" * 60 + "\n")
                
                # Send initial email notification
                send_email(alert_number=1)
                
                # Send reminder emails every 5 minutes for 1 hour
                print("\nSending reminder emails every 5 minutes for the next hour...")
                for i in range(2, 13):  # Alerts 2-12 (total 12 emails over 1 hour)
                    time.sleep(300)  # Wait 5 minutes
                    print(f"\n⚠️  Sending reminder email {i}/12...")
                    send_email(alert_number=i)
                
                print("\n" + "=" * 60)
                print("Alert sequence completed. Monitoring stopped.")
                print("Restart the script if you want to continue monitoring.")
                print("=" * 60)
                break  # Stop monitoring after alert sequence
            
            # Wait before checking again
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("Monitoring stopped by user.")
        print("Run the script again to resume monitoring.")
        print("=" * 60)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("Script crashed. Please restart it.")

if __name__ == "__main__":
    main()
