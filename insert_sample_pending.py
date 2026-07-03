from datetime import datetime

from services.database_service import DatabaseService

db = DatabaseService()

conn = db.connect()
cursor = conn.cursor()

# -------------------------------------------------------
# Resolved Complaints
# -------------------------------------------------------

complaints = [

(
240106,
"013-MT-2025-240106",
13,
"2007CK1188",
datetime.now().strftime("%d-%b-%y"),
"192.168.1.20",
"AA-BB-CC-DD-20",
"SYS-106",
"Outlook crashes",
"Outlook closes immediately after login.",
"L3_ADMIN",
"L3_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"R",
"L3_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"HIGH",
"ISSUE",
1,
"L3",
"L3_ADMIN"
),

(
240107,
"018-NET-2025-240107",
18,
"2006NT1180",
datetime.now().strftime("%d-%b-%y"),
"192.168.1.21",
"AA-BB-CC-DD-21",
"SYS-107",
"VPN not connecting",
"Unable to establish VPN connection.",
"L3_ADMIN",
"L3_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"R",
"L3_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"HIGH",
"ISSUE",
1,
"L3",
"L3_ADMIN"
),

(
240108,
"021-HRMS-2025-240108",
21,
"2008HR1055",
datetime.now().strftime("%d-%b-%y"),
"192.168.1.22",
"AA-BB-CC-DD-22",
"SYS-108",
"Leave approval stuck",
"Leave request remains pending.",
"L1_ADMIN",
"L1_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"R",
"L1_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"LOW",
"ISSUE",
1,
"L1",
"L1_ADMIN"
),

(
240109,
"016-VMS-2025-240109",
16,
"2007CK1194",
datetime.now().strftime("%d-%b-%y"),
"192.168.1.23",
"AA-BB-CC-DD-23",
"SYS-109",
"Face mismatch",
"Another employee photo is displayed.",
"L3_ADMIN",
"L3_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"R",
"L3_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"HIGH",
"ISSUE",
1,
"L3",
"L3_ADMIN"
),

(
240110,
"017-EFILE-2025-240110",
17,
"2004AD1129",
datetime.now().strftime("%d-%b-%y"),
"192.168.1.24",
"AA-BB-CC-DD-24",
"SYS-110",
"File not opening",
"Unable to open eFile after update.",
"L2_ADMIN",
"L2_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"R",
"L2_ADMIN",
datetime.now().strftime("%d-%b-%y"),
"MEDIUM",
"ISSUE",
1,
"L2",
"L2_ADMIN"
)

]

# -------------------------------------------------------
# Insert Complaints
# -------------------------------------------------------

for row in complaints:

    try:

        cursor.execute("""

        INSERT INTO COMPLAIN_SYS_FEED
        (
        SR_NO,
        TICKET_NO,
        ESTT_CODE,
        FED_ECODE,
        FED_DATE,
        FED_IP,
        FED_MAC,
        SYSTEM_NO,
        SUBJECT,
        COMP_BRIEF,
        ASSIGN_TO,
        ASSIGN_BY,
        ASSIGN_DATE,
        STATUS_FLAG,
        RECT_BY,
        RECT_DATE,
        PRIOR_FLAG,
        FLAG_TYPE,
        BKT_FLAG,
        LEVEL_FLAG,
        RECT_ECODE
        )

        VALUES
        (
        :1,:2,:3,:4,:5,:6,:7,:8,:9,:10,
        :11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21
        )

        """, row)

    except Exception as e:

        print(e)

# -------------------------------------------------------
# Conversations
# -------------------------------------------------------

ack = [

# 240106 Outlook
("240106","Outlook crashes immediately after login.","USER"),
("240106","Requested Outlook version and screenshot.","ADMIN"),
("240106","Shared Outlook 2019 screenshot.","USER"),
("240106","Repaired Microsoft Office installation.","ADMIN"),
("240106","Verified Outlook opens successfully.","ADMIN"),

# 240107 VPN
("240107","VPN disconnects during authentication.","USER"),
("240107","Checked VPN gateway logs.","ADMIN"),
("240107","Reset VPN profile.","ADMIN"),
("240107","VPN connected successfully.","USER"),
("240107","Issue resolved after profile reset.","ADMIN"),

# 240108 HRMS
("240108","Leave request pending for three days.","USER"),
("240108","Forwarded request to HRMS support.","ADMIN"),
("240108","Workflow restarted.","ADMIN"),
("240108","Leave approved successfully.","USER"),
("240108","Verified approval completed.","ADMIN"),

# 240109 VMS
("240109","Incorrect employee photo displayed.","USER"),
("240109","Requested cache refresh.","ADMIN"),
("240109","Cache refreshed successfully.","ADMIN"),
("240109","Correct photo displayed now.","USER"),
("240109","Issue resolved after cache update.","ADMIN"),

# 240110 eFile
("240110","Unable to open eFile after latest update.","USER"),
("240110","Verified application logs.","ADMIN"),
("240110","Reinstalled eFile application.","ADMIN"),
("240110","Application working properly.","USER"),
("240110","Verified issue resolved.","ADMIN"),

]

# -------------------------------------------------------
# Insert Acknowledgements
# -------------------------------------------------------

for ticket, remark, flag in ack:

    try:

        cursor.execute("""

        INSERT INTO ACKNOWLEDGEMENT
        (
        ASNO,
        REMARKS,
        FDATE,
        FLAG
        )

        VALUES
        (
        :1,
        :2,
        SYSDATE,
        :3
        )

        """,
        (
            ticket,
            remark,
            flag
        ))

    except Exception as e:

        print(e)

conn.commit()

cursor.close()
conn.close()

print("=" * 60)
print("Resolved Tickets Inserted Successfully")
print("=" * 60)