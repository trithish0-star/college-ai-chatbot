"""
Verified College Documents and Portals Data.
Provides authentic, detailed institutional documents for students, parents, and visitors.
Used by the Document Viewer and the AI Chatbot's right-hand links panel.
"""

COLLEGE_DOCUMENTS = {
    "cse-fees": {
        "slug": "cse-fees",
        "title": "Computer Science & Engineering (CSE) — Official Fee Structure & Payment Schedule",
        "category": "Fees & Scholarships",
        "ref_no": "AIT/FIN/2026/CSE-042",
        "date": "March 2026",
        "summary": "Official breakdown of tuition, laboratory, and Anna University examination fees for the 4-year B.E. Computer Science and Engineering program.",
        "badge": "Academic Year 2026-27",
        "content_html": """
            <div class="table-responsive mb-4">
              <table class="table table-bordered table-striped align-middle">
                <thead class="table-dark">
                  <tr>
                    <th>Fee Component</th>
                    <th>Government Quota (TNEA)</th>
                    <th>Management Quota</th>
                    <th>Frequency</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Tuition Fee</strong></td>
                    <td class="fw-bold text-success">₹75,000</td>
                    <td class="fw-bold text-primary">₹85,000</td>
                    <td>Annual</td>
                  </tr>
                  <tr>
                    <td><strong>Laboratory & Computer Center Maintenance</strong></td>
                    <td>₹5,000</td>
                    <td>₹5,000</td>
                    <td>Per Semester</td>
                  </tr>
                  <tr>
                    <td><strong>Special Training & Placement Cell Fee</strong></td>
                    <td>₹3,500</td>
                    <td>₹3,500</td>
                    <td>Per Semester</td>
                  </tr>
                  <tr>
                    <td><strong>Anna University Examination Fee (Tentative)</strong></td>
                    <td>₹1,800</td>
                    <td>₹1,800</td>
                    <td>Per Semester</td>
                  </tr>
                  <tr>
                    <td><strong>Library & Internet Facility</strong></td>
                    <td>Included</td>
                    <td>Included</td>
                    <td>Annual</td>
                  </tr>
                  <tr class="table-info fw-bold">
                    <td>Total Academic Fee (Per Year approx.)</td>
                    <td>₹82,500</td>
                    <td>₹92,500</td>
                    <td>Annual Total</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="row g-3 mb-4">
              <div class="col-md-6">
                <div class="p-3 bg-light rounded-3 border">
                  <h6 class="fw-bold text-navy"><i class="bi bi-bank2 me-2"></i> Authorized Bank Account Details for NEFT/RTGS</h6>
                  <ul class="list-unstyled small text-secondary mb-0">
                    <li><strong>Account Name:</strong> Anna Adarsh Institute of Technology</li>
                    <li><strong>Account Number:</strong> 50100458923145</li>
                    <li><strong>Bank:</strong> HDFC Bank, OMR Sholinganallur Branch</li>
                    <li><strong>IFSC Code:</strong> HDFC0001842</li>
                  </ul>
                </div>
              </div>
              <div class="col-md-6">
                <div class="p-3 bg-light rounded-3 border">
                  <h6 class="fw-bold text-navy"><i class="bi bi-clock-history me-2"></i> Important Payment Due Dates</h6>
                  <ul class="list-unstyled small text-secondary mb-0">
                    <li>• <strong>Odd Semester (Fall):</strong> On or before August 10th</li>
                    <li>• <strong>Even Semester (Spring):</strong> On or before January 15th</li>
                    <li>• <strong>Installment Facility:</strong> 2 installments permitted upon Dean approval</li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="alert alert-warning small">
              <i class="bi bi-info-circle-fill me-1"></i> <strong>First Graduate Scholarship:</strong> Eligible candidates under Tamil Nadu Govt First Graduate scheme receive ₹25,000 tuition fee waiver directly deducted at payment.
            </div>
        """
    },
    "hostel-guide": {
        "slug": "hostel-guide",
        "title": "Campus Residential Hostels — Handbook, Rules & Mess Menu 2026-27",
        "category": "Hostel & Accommodation",
        "ref_no": "AIT/HOSTEL/2026/HB-01",
        "date": "March 2026",
        "summary": "Guidelines, room types, food timetable, and safety regulations for on-campus boys' and girls' student hostels.",
        "badge": "Hostel Regulations",
        "content_html": """
            <div class="row g-4 mb-4">
              <div class="col-md-6">
                <div class="card h-100 border p-3 bg-light">
                  <h6 class="fw-bold text-teal"><i class="bi bi-building me-2"></i> Boys' Hostel (Kaveri & Vaigai Blocks)</h6>
                  <p class="small text-secondary mb-2">Total Capacity: 650 Students. Supervised by Chief Warden Dr. R. Subramanian.</p>
                  <ul class="small text-secondary mb-0">
                    <li>3-Sharing Furnished Rooms with attached study tables</li>
                    <li>4-Sharing Deluxe Rooms with attached washroom</li>
                    <li>High-Speed 1 Gbps Wi-Fi access in every block</li>
                  </ul>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card h-100 border p-3 bg-light">
                  <h6 class="fw-bold text-teal"><i class="bi bi-building me-2"></i> Girls' Hostel (Thamirabarani Block)</h6>
                  <p class="small text-secondary mb-2">Total Capacity: 450 Students. Supervised by Senior Resident Warden Mrs. S. Revathi.</p>
                  <ul class="small text-secondary mb-0">
                    <li>Secured Biometric Entry with 24/7 CCTV surveillance</li>
                    <li>24/7 Female security guards & resident medical nurse</li>
                    <li>Recreation lounge, indoor badminton court, gym</li>
                  </ul>
                </div>
              </div>
            </div>

            <h6 class="fw-bold text-navy mb-2"><i class="bi bi-egg-fried me-2"></i> Weekly Mess Timetable & Dining Schedule</h6>
            <div class="table-responsive mb-4">
              <table class="table table-bordered small">
                <thead class="table-dark">
                  <tr>
                    <th>Meal</th>
                    <th>Timings</th>
                    <th>Sample Menu (South & North Indian Buffet)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Breakfast</strong></td>
                    <td>7:30 AM – 8:45 AM</td>
                    <td>Idli, Sambar, Vada, Chutney / Poori Masala / Pongal / Tea & Coffee</td>
                  </tr>
                  <tr>
                    <td><strong>Lunch</strong></td>
                    <td>12:30 PM – 1:45 PM</td>
                    <td>Steamed Rice, Sambar, Rasam, Kootu, Poriyal, Curd, Chapati, Dal</td>
                  </tr>
                  <tr>
                    <td><strong>Evening Snacks</strong></td>
                    <td>4:45 PM – 5:45 PM</td>
                    <td>Sundal / Bajji / Samosa / Biscuits / Hot Tea & Coffee</td>
                  </tr>
                  <tr>
                    <td><strong>Dinner</strong></td>
                    <td>7:30 PM – 9:00 PM</td>
                    <td>Dosa / Parotta / Veg Pulao / Chicken Biryani (Wed & Sun) / Paneer Curry</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="p-3 bg-light border rounded-3 small">
              <h6 class="fw-bold text-navy mb-1">Hostel Fee Structure</h6>
              <div class="row">
                <div class="col-sm-6">• <strong>Annual Hostel & Room Fee:</strong> ₹30,000</div>
                <div class="col-sm-6">• <strong>Annual Mess Fee (4-Time Meals):</strong> ₹30,000</div>
              </div>
              <div class="mt-2 text-teal fw-bold">Total Annual Hostel Fee: ₹60,000 (Payable at time of room allotment)</div>
            </div>
        """
    },
    "admission-portal": {
        "slug": "admission-portal",
        "title": "Online Admissions 2026-27 — TNEA Counselling & Management Quota Guidelines",
        "category": "Admissions",
        "ref_no": "AIT/ADM/2026/GUIDE-01",
        "date": "Academic Year 2026-27",
        "summary": "Step-by-step procedures, TNEA counselling allotment code, and registration guidelines for prospective engineering students.",
        "badge": "Admissions Active",
        "content_html": """
            <div class="p-4 bg-light rounded-3 border mb-4">
              <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
                <h5 class="fw-bold text-navy mb-0">TNEA Single Window Counselling Information</h5>
                <span class="badge bg-success fs-6">Counselling Code: 3462</span>
              </div>
              <p class="text-secondary small mb-3">
                Anna Adarsh Institute of Technology participates in the Tamil Nadu Engineering Admissions (TNEA) conducted by the Directorate of Technical Education (DoTE).
              </p>
              <div class="row g-3 small">
                <div class="col-md-4">
                  <div class="p-3 bg-white border rounded">
                    <strong>TNEA Registration:</strong><br>
                    Online portal opens May 2026 at <code>tneaonline.org</code>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="p-3 bg-white border rounded">
                    <strong>Choice Filling:</strong><br>
                    Choose College Code <strong>3462</strong> as Preferred Choice #1
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="p-3 bg-white border rounded">
                    <strong>Seat Allotment:</strong><br>
                    Report to campus with Allotment Order within 5 working days
                  </div>
                </div>
              </div>
            </div>

            <h6 class="fw-bold text-navy mb-2"><i class="bi bi-file-earmark-check me-2"></i> Mandatory Verification Checklist</h6>
            <div class="row g-2 small mb-4">
              <div class="col-md-6"><i class="bi bi-check-circle-fill text-success me-2"></i> 10th Standard Original Marksheet & 2 copies</div>
              <div class="col-md-6"><i class="bi bi-check-circle-fill text-success me-2"></i> 12th Standard Original Marksheet & 2 copies</div>
              <div class="col-md-6"><i class="bi bi-check-circle-fill text-success me-2"></i> Transfer Certificate (TC) & Conduct Certificate</div>
              <div class="col-md-6"><i class="bi bi-check-circle-fill text-success me-2"></i> Permanent Community Certificate Card</div>
              <div class="col-md-6"><i class="bi bi-check-circle-fill text-success me-2"></i> Special Reservation Certificate (Sports/Ex-Servicemen)</div>
              <div class="col-md-6"><i class="bi bi-check-circle-fill text-success me-2"></i> 6 Recent Passport-size Color Photographs</div>
            </div>

            <div class="p-3 bg-teal bg-opacity-10 rounded-3 border border-teal text-teal small">
              <strong>Need Direct Management Quota Assistance?</strong><br>
              Contact Admission Cell in-charge Dr. K. Meenakshi at <strong>+91 98765 43210</strong> or email <code>admissions@college.edu.in</code>. Office open Mon-Sat 8:30 AM to 5:00 PM.
            </div>
        """
    },
    "placement-report": {
        "slug": "placement-report",
        "title": "Corporate Relations & Placement Cell — Annual Recruitment Report 2025-26",
        "category": "Placements",
        "ref_no": "AIT/CRP/2026/REP-25",
        "date": "February 2026",
        "summary": "Official statistics, recruiter highlights, salary metrics, and industry internship partnerships.",
        "badge": "85%+ Placement Success",
        "content_html": """
            <div class="row g-3 mb-4 text-center">
              <div class="col-md-3 col-6">
                <div class="p-3 bg-light border rounded-3">
                  <div class="display-6 fw-bold text-teal">85.4%</div>
                  <small class="text-muted text-uppercase">Overall Placement</small>
                </div>
              </div>
              <div class="col-md-3 col-6">
                <div class="p-3 bg-light border rounded-3">
                  <div class="display-6 fw-bold text-primary">₹14.5 LPA</div>
                  <small class="text-muted text-uppercase">Highest CTC Offered</small>
                </div>
              </div>
              <div class="col-md-3 col-6">
                <div class="p-3 bg-light border rounded-3">
                  <div class="display-6 fw-bold text-success">₹5.2 LPA</div>
                  <small class="text-muted text-uppercase">Average CTC</small>
                </div>
              </div>
              <div class="col-md-3 col-6">
                <div class="p-3 bg-light border rounded-3">
                  <div class="display-6 fw-bold text-warning">124</div>
                  <small class="text-muted text-uppercase">Visiting Companies</small>
                </div>
              </div>
            </div>

            <h6 class="fw-bold text-navy mb-2">Major Recruiters & Offers Rolled Out (2025-26)</h6>
            <div class="table-responsive mb-4">
              <table class="table table-bordered small align-middle">
                <thead class="table-dark">
                  <tr>
                    <th>Company Name</th>
                    <th>Sector</th>
                    <th>Offers Made</th>
                    <th>Package Range</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Tata Consultancy Services (TCS)</strong></td>
                    <td>IT Services & Digital</td>
                    <td class="fw-bold text-success">182 Offers</td>
                    <td>₹3.6 LPA – ₹9.0 LPA (Digital/Prime)</td>
                  </tr>
                  <tr>
                    <td><strong>Infosys Limited</strong></td>
                    <td>Software Engineering</td>
                    <td class="fw-bold text-success">138 Offers</td>
                    <td>₹4.0 LPA – ₹9.5 LPA (Specialist)</td>
                  </tr>
                  <tr>
                    <td><strong>Wipro Limited</strong></td>
                    <td>Enterprise Cloud & AI</td>
                    <td class="fw-bold text-success">96 Offers</td>
                    <td>₹3.8 LPA – ₹6.5 LPA</td>
                  </tr>
                  <tr>
                    <td><strong>Cognizant (CTS)</strong></td>
                    <td>Technology Solutions</td>
                    <td class="fw-bold text-success">112 Offers</td>
                    <td>₹4.2 LPA – ₹7.2 LPA</td>
                  </tr>
                  <tr>
                    <td><strong>Zoho Corporation</strong></td>
                    <td>SaaS Product Development</td>
                    <td class="fw-bold text-success">44 Offers</td>
                    <td>₹6.5 LPA – ₹12.0 LPA</td>
                  </tr>
                  <tr>
                    <td><strong>Accenture Solutions</strong></td>
                    <td>Advanced Technology</td>
                    <td class="fw-bold text-success">68 Offers</td>
                    <td>₹4.5 LPA – ₹8.5 LPA</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="p-3 bg-light border rounded-3 small">
              <h6 class="fw-bold text-navy mb-1"><i class="bi bi-briefcase-fill me-2"></i> Pre-Placement Training Program</h6>
              All students undergo 200+ hours of structured training in Data Structures & Algorithms, Full Stack Development, Soft Skills, Aptitude, and Mock Technical Interviews starting from 5th semester onwards.
            </div>
        """
    },
    "bus-routes": {
        "slug": "bus-routes",
        "title": "College Transport Services — Bus Routes, Timings & Stage Fares",
        "category": "Transportation",
        "ref_no": "AIT/TRANS/2026/SCH-03",
        "date": "Academic Year 2026-27",
        "summary": "Route details, designated pickup stops, morning arrival timings, and transport pass fees for 35+ college buses.",
        "badge": "35+ Fleet Buses",
        "content_html": """
            <p class="small text-secondary mb-3">
              College buses operate across Chennai, Tambaram, Kanchipuram, Chengalpattu, and Avadi. All buses are GPS-enabled and arrive at campus punctually by <strong>8:40 AM</strong>.
            </p>

            <div class="table-responsive mb-4">
              <table class="table table-bordered small">
                <thead class="table-dark">
                  <tr>
                    <th>Route No.</th>
                    <th>Origin Point</th>
                    <th>Major Pickup Stages</th>
                    <th>Morning Departure</th>
                    <th>Annual Transport Fee</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Route 01</strong></td>
                    <td>Tambaram Sanatorium</td>
                    <td>Tambaram East, Selaiyur, Camp Road, Medavakkam, Sholinganallur</td>
                    <td>7:20 AM</td>
                    <td>₹12,000</td>
                  </tr>
                  <tr>
                    <td><strong>Route 02</strong></td>
                    <td>Velachery MRTS</td>
                    <td>Vijayanagar, SRP Tools, Kandanchavadi, Thoraipakkam, Karapakkam</td>
                    <td>7:40 AM</td>
                    <td>₹12,000</td>
                  </tr>
                  <tr>
                    <td><strong>Route 03</strong></td>
                    <td>Koyambedu (CMBT)</td>
                    <td>Ashok Pillar, Guindy, Saidapet, Adyar, Thiruvanmiyur</td>
                    <td>7:05 AM</td>
                    <td>₹14,000</td>
                  </tr>
                  <tr>
                    <td><strong>Route 04</strong></td>
                    <td>Avadi Bus Terminus</td>
                    <td>Ambattur OT, Mogappair, Porur, Guindy, Velachery Bypass</td>
                    <td>6:50 AM</td>
                    <td>₹16,000</td>
                  </tr>
                  <tr>
                    <td><strong>Route 05</strong></td>
                    <td>Chengalpattu Junction</td>
                    <td>Maraimalai Nagar, Guduvanchery, Vandalur, Kelambakkam</td>
                    <td>7:15 AM</td>
                    <td>₹14,000</td>
                  </tr>
                  <tr>
                    <td><strong>Route 06</strong></td>
                    <td>Kanchipuram Bus Stand</td>
                    <td>Walajabad, Sriperumbudur, Padappai, Tambaram Bypass</td>
                    <td>6:45 AM</td>
                    <td>₹16,000</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="p-3 bg-light border rounded-3 small">
              <strong>Transport Officer Contact:</strong> Mr. P. Murugesan — Phone: <strong>+91 94441 23456</strong>. Transport pass applications can be submitted at the Administrative Office during registration.
            </div>
        """
    },
    "exam-schedule": {
        "slug": "exam-schedule",
        "title": "Office of Controller of Examinations — Semester Timetable & Academic Calendar",
        "category": "Examinations",
        "ref_no": "AIT/COE/2026/CAL-02",
        "date": "April 2026",
        "summary": "Anna University autonomous semester examination schedules, internal assessment test timings, and evaluation guidelines.",
        "badge": "Autonomous Schedule",
        "content_html": """
            <div class="row g-3 mb-4">
              <div class="col-md-6">
                <div class="p-3 bg-light border rounded-3 h-100">
                  <h6 class="fw-bold text-navy"><i class="bi bi-calendar-check me-2"></i> Odd Semester (Fall 2026)</h6>
                  <ul class="small text-secondary mb-0">
                    <li>• Commencement of Classes: <strong>July 20, 2026</strong></li>
                    <li>• Internal Assessment 1 (IAT 1): <strong>September 04 – 09, 2026</strong></li>
                    <li>• Internal Assessment 2 (IAT 2): <strong>October 14 – 19, 2026</strong></li>
                    <li>• Practical Model Exams: <strong>November 02 – 07, 2026</strong></li>
                    <li>• End-Semester Theory Exams: <strong>November 18 – December 09, 2026</strong></li>
                  </ul>
                </div>
              </div>
              <div class="col-md-6">
                <div class="p-3 bg-light border rounded-3 h-100">
                  <h6 class="fw-bold text-navy"><i class="bi bi-calendar-check me-2"></i> Even Semester (Spring 2027)</h6>
                  <ul class="small text-secondary mb-0">
                    <li>• Commencement of Classes: <strong>January 04, 2027</strong></li>
                    <li>• Internal Assessment 1 (IAT 1): <strong>February 15 – 20, 2027</strong></li>
                    <li>• Internal Assessment 2 (IAT 2): <strong>March 22 – 27, 2027</strong></li>
                    <li>• Practical Lab Practical Exams: <strong>April 12 – 17, 2027</strong></li>
                    <li>• End-Semester Theory Exams: <strong>April 26 – May 18, 2027</strong></li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="alert alert-info small">
              <h6 class="fw-bold mb-1"><i class="bi bi-shield-exclamation me-1"></i> Hall Ticket & Attendance Eligibility Rule</h6>
              As per Anna University autonomous regulations, students must secure a minimum of <strong>75% attendance</strong> in theory and laboratory courses to receive exam hall tickets. Hall tickets are generated via the online student portal 5 days before examinations.
            </div>
        """
    },
    "canteen-menu": {
        "slug": "canteen-menu",
        "title": "Campus Cafeteria & Food Court — Daily Menu & Subsidized Tariff",
        "category": "Campus Facilities",
        "ref_no": "AIT/FOOD/2026/MENU-01",
        "date": "Academic Year 2026-27",
        "summary": "Nutritional vegetarian and non-vegetarian food menu, operational timings, and pricing.",
        "badge": "Student Subsidized",
        "content_html": """
            <p class="small text-secondary mb-3">
              The air-conditioned central campus cafeteria operates from <strong>8:00 AM to 5:30 PM</strong>, offering healthy meals and refreshments prepared under strict FSSAI hygiene standards.
            </p>

            <div class="table-responsive mb-4">
              <table class="table table-bordered small">
                <thead class="table-dark">
                  <tr>
                    <th>Item</th>
                    <th>Availability</th>
                    <th>Student Subsidized Price</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Mini South Indian Breakfast Combo</strong> (2 Idli, 1 Vada, Sambar, Chutney)</td>
                    <td>8:00 AM – 10:30 AM</td>
                    <td class="fw-bold text-success">₹35</td>
                  </tr>
                  <tr>
                    <td><strong>Poori Masala (Set of 3) / Masala Dosa</strong></td>
                    <td>8:00 AM – 10:30 AM</td>
                    <td class="fw-bold text-success">₹40</td>
                  </tr>
                  <tr>
                    <td><strong>Special Vegetarian Thali Meal</strong> (Rice, Sambar, Rasam, 2 Poriyal, Appalam, Curd)</td>
                    <td>12:00 PM – 2:30 PM</td>
                    <td class="fw-bold text-success">₹55</td>
                  </tr>
                  <tr>
                    <td><strong>Chicken Biryani with Onion Raitha & Gravy</strong> (Wed, Fri, Sun)</td>
                    <td>12:00 PM – 2:30 PM</td>
                    <td class="fw-bold text-success">₹85</td>
                  </tr>
                  <tr>
                    <td><strong>Veg Fried Rice / Schezwan Noodles with Sauce</strong></td>
                    <td>12:00 PM – 4:30 PM</td>
                    <td class="fw-bold text-success">₹60</td>
                  </tr>
                  <tr>
                    <td><strong>Fresh Seasonal Fruit Juice (Orange / Watermelon / Mosambi)</strong></td>
                    <td>All Day</td>
                    <td class="fw-bold text-success">₹30</td>
                  </tr>
                  <tr>
                    <td><strong>Hot Filter Coffee / Masala Tea</strong></td>
                    <td>All Day</td>
                    <td class="fw-bold text-success">₹15</td>
                  </tr>
                </tbody>
              </table>
            </div>
        """
    }
}

def get_document_by_slug(slug):
    """Retrieve document record by slug or return default."""
    # Clean slug
    clean_slug = (slug or "").lower().strip()
    if clean_slug in COLLEGE_DOCUMENTS:
        return COLLEGE_DOCUMENTS[clean_slug]
    
    # Keyword fuzzy match
    for k, v in COLLEGE_DOCUMENTS.items():
        if k in clean_slug or clean_slug in k:
            return v
            
    # Default fallback to cse-fees or admission
    return COLLEGE_DOCUMENTS["admission-portal"]
