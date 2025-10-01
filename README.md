# 🧩 DE-Lost&Found Prototype

A campus/community **Lost & Found platform** prototype where the main focus is on the **AI/ML system for matching items** (text + images).

---

## 🎯 Core Idea

Help students/staff find lost belongings by **matching lost item descriptions/images with reported found items** using similarity models.

---

## ✅ Progress So Far

- Built a **basic prototype** using:
  - JSON/dummy data as storage.
  - **Cosine similarity** on item descriptions for matching lost & found reports.
- Implemented:
  - Report a *Found* item.
  - Search for a *Lost* item by description/place.
  - Show best matches from the stored data.

---

## 🚀 Next Goals

1. **Database Integration**
   - Use a proper DB (e.g., MongoDB or PostgreSQL + vector search) for storing found items.
   - Lost items:
     - First try matching immediately.
     - If not found, user can save lost item report in DB for later matches.

2. **AI/ML Matching**
   - Upgrade from cosine similarity → **CLIP model** for:
     - **Text-to-Image** matching.
     - **Image-to-Text** matching.
   - Lightweight setup for local experimentation.

3. **Notifications**
   - Notify the user if their lost item gets matched later with a newly reported found item.

4. **Ownership Verification**
   - Final confirmation step: founder and claimant communicate directly to verify ownership.
   - Simple manual step (no automation needed for prototype).

---

## 📌 Tech Stack (Prototype Stage)

- **Backend**: Python (FastAPI planned)  
- **Database**: Initially JSON → MongoDB (next stage)  
- **ML Models**: 
  - Stage 1: Cosine similarity on text embeddings  
  - Stage 2: CLIP (text ↔ image matching)  

---

## 🛠 Roadmap

- [x] Basic cosine similarity prototype with dummy data  
- [ ] Integrate database for storing found/lost items  
- [ ] Implement CLIP for image + text similarity search  
- [ ] Add notification system for delayed matches  
- [ ] Simple ownership verification flow  

---

