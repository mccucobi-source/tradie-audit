# Complete Customer Journey - Tradie Audit Agent

## The Full Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CUSTOMER JOURNEY                                    │
└─────────────────────────────────────────────────────────────────────────────┘

   ACQUISITION              INTAKE                 PROCESSING              DELIVERY
   ───────────             ─────────              ────────────             ────────
       │                       │                       │                       │
       ▼                       ▼                       ▼                       ▼
┌─────────────┐       ┌─────────────────┐      ┌─────────────┐       ┌─────────────┐
│  Customer   │       │  Customer fills │      │  AI Agents  │       │  You review │
│  pays $797  │ ───▶  │  intake form    │ ───▶ │  run audit  │ ───▶  │  & deliver  │
│  (Stripe)   │       │  (15 mins)      │      │  (~30 secs) │       │  (30 mins)  │
└─────────────┘       └─────────────────┘      └─────────────┘       └─────────────┘
                              │                       │
                              ▼                       ▼
                      ┌───────────────┐       ┌───────────────┐
                      │ Uploads docs: │       │ Generates:    │
                      │ • Invoices    │       │ • HTML Report │
                      │ • Expenses    │       │ • Excel Book  │
                      │ • Statements  │       │ • Action Plan │
                      │ • Quotes      │       └───────────────┘
                      └───────────────┘
```

---

## Step-by-Step Breakdown

### 1. Customer Acquisition
**Where:** Facebook groups, LinkedIn, direct outreach, referrals
**What happens:** 
- Customer books free 15-min "profit check" call
- You assess fit and explain the offer
- They pay $797 via Stripe

**Your time:** 15-30 mins

---

### 2. Customer Intake (The Portal)
**Where:** `streamlit run src/customer_portal.py`
**URL:** You send them a link like `https://audit.yourdomain.com`

**What they fill out:**

#### Step 1: Business Details (2 mins)
- Business name
- Owner name & email
- Trade type (electrician, plumber, etc.)
- Location (Sydney, Melbourne, etc.)
- Years in business

#### Step 2: Current Numbers (3 mins)
- Approximate annual revenue
- Current hourly rate
- Call-out fee (if any)
- Material markup
- Hours worked per week
- Team size

#### Step 3: Goals & Challenges (2 mins)
- Revenue goal
- Ideal work hours
- Main frustrations (checklist)
- #1 question they want answered

#### Step 4: Document Upload (5-10 mins)
- **Invoices** (Required) - Last 12 months
- **Expenses** (Required) - Materials, fuel, tools, etc.
- **Bank Statements** (Recommended) - Shows real cash flow
- **Quotes** (If available) - Won AND lost quotes

#### Step 5: Final Details (1 min)
- Accounting software used
- Preferred contact method
- Best time for call
- Anything else relevant

**Customer's time:** ~15 minutes
**Your time:** 0 (automated)

---

### 3. Automatic Processing
**Where:** Runs automatically when they submit
**What happens:**

```
Customer hits "Submit"
         │
         ▼
┌─────────────────────────────┐
│  DATA EXTRACTION AGENT      │
│  • Reads all uploaded files │
│  • Extracts transactions    │
│  • Structures the data      │
│  Cost: ~$0.05-0.10          │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  ANALYSIS AGENT             │
│  • Calculates metrics       │
│  • Compares to benchmarks   │
│  • Finds profit leaks       │
│  • Generates 10 actions     │
│  Cost: ~$0.03-0.05          │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  REPORT GENERATOR           │
│  • Creates HTML report      │
│  • Creates Excel workbook   │
│  • Writes exec summary      │
│  Cost: ~$0.01-0.02          │
└─────────────────────────────┘
         │
         ▼
    AUDIT COMPLETE
    Total time: ~30 seconds
    Total cost: ~$0.10-0.20
```

---

### 4. Your Review (The Human Touch)
**Where:** `streamlit run src/admin_dashboard.py`
**What you do:**

1. **Open the admin dashboard**
   - See all pending audits
   - Click to view results

2. **Review the analysis** (10-15 mins)
   - Check the numbers make sense
   - Verify recommendations are appropriate
   - Add any personal insights

3. **Optional: Record a Loom video** (10 mins)
   - Walk through the key findings
   - Explain top 3 actions
   - Add personal touch

4. **Send to customer**
   - Email the HTML report
   - Attach Excel workbook
   - Include Loom link
   - Book strategy call

**Your time:** 30-45 mins total

---

### 5. Strategy Call & Follow-up
**What happens:**
- 60-min Zoom call to discuss findings
- Answer questions
- Help prioritize actions
- Set 30/60/90 day check-in dates

**Your time:** 60-90 mins

---

## Time Comparison

| Step | Manual (Before) | Automated (After) |
|------|-----------------|-------------------|
| Intake form | 30 mins call | 0 mins (self-serve) |
| Data processing | 4-6 hours | 30 seconds |
| Analysis | 8-10 hours | 30 seconds |
| Report writing | 4-6 hours | 30 seconds |
| Review & personalize | 2-3 hours | 30-45 mins |
| Strategy call | 60-90 mins | 60-90 mins |
| **TOTAL** | **~20 hours** | **~2 hours** |

---

## Running the System

### Start Customer Portal (for customers)
```bash
streamlit run src/customer_portal.py --server.port 8502
```
Access at: http://localhost:8502

### Start Admin Dashboard (for you)
```bash
streamlit run src/admin_dashboard.py --server.port 8503
```
Access at: http://localhost:8503

### Or run both at once
```bash
# Terminal 1
streamlit run src/customer_portal.py --server.port 8502

# Terminal 2
streamlit run src/admin_dashboard.py --server.port 8503
```

---

## Deployment Options

### Option A: Run Locally (Free)
- Run on your laptop
- Send customers direct link when on call
- Best for starting out

### Option B: Deploy to Streamlit Cloud (Free)
1. Push code to GitHub
2. Connect to share.streamlit.io
3. Get public URL
4. Cost: Free (but shows Streamlit branding)

### Option C: Deploy to Railway/Render ($5-20/month)
1. Push to GitHub
2. Connect to Railway or Render
3. Custom domain
4. Cost: $5-20/month

### Option D: Deploy to VPS ($10-20/month)
1. Get DigitalOcean/Linode VPS
2. Install dependencies
3. Run with supervisor/systemd
4. Custom domain + SSL
5. Most professional option

---

## Sample Customer Email Sequence

### Email 1: Payment Confirmation
```
Subject: ✅ Payment Received - Let's Find Your Profit Leaks

G'day [Name],

Thanks for signing up for the Profit Leak Audit!

Here's what happens next:

1. **Fill out the intake form** (takes ~15 mins)
   👉 [Link to customer portal]

2. **Upload your documents**
   - Invoices (last 12 months)
   - Expenses/bank statements
   - Quotes if you have them

3. **We analyze everything** (takes us 7 days)

4. **You get your report + strategy call**

The sooner you complete the form, the sooner we find your profit leaks.

Any questions, just reply to this email.

Cheers,
[Your name]
```

### Email 2: Reminder (if not submitted after 2 days)
```
Subject: Quick reminder - your Profit Leak Audit

Hey [Name],

Just checking in - haven't seen your documents come through yet.

Most tradies find 15 minutes during smoko to knock this out.

Here's the link again: [Link]

If you're stuck on anything, hit reply and I'll help.

Cheers,
[Your name]
```

### Email 3: Report Delivery
```
Subject: 🔥 Your Profit Leak Audit is Ready - $XX,XXX Found

[Name],

Your audit is done. Here's what we found:

💰 **Total Opportunity: $XX,XXX/year**

Top 3 Quick Wins:
1. [Action 1] - $X,XXX/year
2. [Action 2] - $X,XXX/year
3. [Action 3] - $X,XXX/year

**Your Report:** [Attached / Link]
**Action Workbook:** [Attached / Link]
**Video Walkthrough:** [Loom link]

Let's book your strategy call to go through this together:
👉 [Calendly link]

This is where it gets good.

Cheers,
[Your name]
```

---

## Cost Per Audit (Full Breakdown)

| Item | Cost |
|------|------|
| Claude API (extraction) | $0.05-0.10 |
| Claude API (analysis) | $0.03-0.05 |
| Claude API (summary) | $0.01-0.02 |
| Hosting (amortized) | ~$0.50 |
| Your time (2 hrs @ $100/hr value) | $200 |
| **Total Cost** | **~$200** |
| **Revenue** | **$797** |
| **Profit** | **~$597** |
| **Margin** | **75%** |

If you value your time at $50/hr: Profit = $697 (87% margin)

---

## Scaling Path

| Month | Audits | Revenue | Your Time | Effective Hourly |
|-------|--------|---------|-----------|------------------|
| 1 | 10 | $7,970 | 20 hrs | $399/hr |
| 2 | 15 | $11,955 | 30 hrs | $399/hr |
| 3 | 25 | $19,925 | 50 hrs | $399/hr |
| 6 | 40 | $31,880 | 80 hrs | $399/hr |

At 40 audits/month, you're making $32k while working 80 hours (20 hrs/week).

That's a $380k/year business working part-time hours.

---

## Next Steps

1. ✅ Run a test audit to see the flow
2. ✅ Customize the intake form for your branding
3. ✅ Set up Stripe payment link
4. ✅ Connect Calendly for booking
5. ✅ Start selling!

