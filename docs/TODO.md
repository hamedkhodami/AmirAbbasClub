# 🚀 Project TODO – AmirAbbasClub

## TODO List
### accounts
- implement role-based access (Coach, Superuser)
- complete tests for user creation and permissions
- configure Django Admin for coaches and superusers

### payments
- implement Payment model (amount, date, status)
- add admin filters for paid/due
- write tests for payment creation and aggregation

### reports
- implement income aggregation (total fees)
- list athletes with due payments
- add simple date-range summaries
- write unit tests for report queries

### public
- create static pages (club intro, contact, rules)
- integrate base template with TailwindCSS
- add minimal navigation

---

## 🧭 Phase 1 – Initial Implementation

| Step | Title                                      | Status |
|-----:|--------------------------------------------|--------|
| 1️⃣   | Project Architecture Setup (settings, structure) | ✅     |
| 2️⃣   | Testing & Pre-commit Setup (pytest, coverage, hooks) | ✅     |
| 3️⃣   | Core App – Shared Models, Mixins, Utilities | ✅     |
| 4️⃣   | Database Modeling Based on User Stories    | ✅     |
| 5️⃣   | Account App – Roles & Admin                | 🎯     |
| 6️⃣   | Payment App – Fee Records & Status         | 📌     |
| 7️⃣   | Reports App – Income & Debt Dashboards     | 📌     |
| 8️⃣   | Public App – Minimal Pages                 | 📌     |
| 9️⃣   | Phase 1 Summary & Transition               | 📌     |

---

📌 **Legend**  
- 🎯 In Progress  
- 📌 Not Started  
- 🔗 Blocked / Waiting  
- ✅ Completed