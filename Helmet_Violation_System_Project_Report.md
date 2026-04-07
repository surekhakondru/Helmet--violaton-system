# Helmet Violation Detection and Automated Notification System
## Full Project Documentation (Academic Report Structure)

**Note on length:** This report is written for conversion to a standard academic Word template (e.g., A4, Times New Roman 12 pt, 1.15 line spacing, normal margins). The body text below is approximately **9,000–10,500 words**, which typically yields **about 28–34 pages** including front matter, tables, figure captions, and chapter headings—adjust spacing or add institution-specific pages to reach exactly thirty pages.

---

## Title Page

**HELMET VIOLATION DETECTION AND AUTOMATED NOTIFICATION SYSTEM**

A Project Report submitted in partial fulfillment of the requirements for the degree of [Bachelor/Master of Technology / MCA]

**by**  
[Student Name]  
[Roll Number]

**Department of [Computer Science / Engineering]**  
[College / University Name]  
[Month Year]

---

## Certificate

This is to certify that the project work entitled **“Helmet Violation Detection and Automated Notification System”** is a bonafide work carried out by **[Student Name]** **[Roll Number]** under my supervision in partial fulfillment of the requirements for the award of **[Degree Name]** in **[Branch]** at **[Institution]**, during the academic year **[Year–Year]**.

**Supervisor**  
[Name, Designation]  
[Department]

**Head of Department**  
[Name]  
[Department]

**Place:** _______________  
**Date:** _______________

---

## Declaration

I hereby declare that the project report entitled **“Helmet Violation Detection and Automated Notification System”** submitted to **[Institution]** is a record of original work done by me under the supervision of **[Supervisor Name]**, and this work has not been submitted elsewhere for any other degree or diploma.

**Place:** _______________  
**Date:** _______________  
**Signature of the Student**  
**Name:** _______________

---

## Acknowledgement

I express my sincere gratitude to **[Supervisor Name]** for continual guidance, constructive feedback, and support throughout this project. I thank **[HOD Name]** and the faculty of **[Department]** for providing infrastructure and academic resources. I am thankful to my family and friends for their encouragement. Finally, I acknowledge the authors of open datasets, the Ultralytics YOLO ecosystem, and the open-source communities behind Flask, Flutter, OpenCV, and OCR libraries that made rapid prototyping possible.

---

## Abstract

Road safety enforcement for two-wheeler riders remains a persistent challenge in dense urban traffic. Manual surveillance is costly, inconsistent across locations, and difficult to scale. This project presents an **integrated helmet violation detection and notification system** that combines **computer vision**, **automatic number plate recognition (ANPR)**, **structured violation storage**, **analytics**, and **multi-channel alerts** (SMS and WhatsApp via Twilio).

The backend is implemented as a **RESTful Flask API** that accepts images from traffic cameras, IP cameras, a dedicated **video stream processor**, or a **Flutter mobile client**. **Helmet status** is inferred using a **YOLOv8**-based detector configured for classes such as *with helmet* and *without helmet*, with conservative behavior when a specialized helmet model is unavailable (fallback modes avoid false penalties). **License plates** are read using **PaddleOCR** when available or **EasyOCR** as fallback, with normalization and pattern checks suited to Indian plate formats. On confirmed violations, the system stores an **annotated evidence image**, persists a **violation record** (default storage: **SQLite** via SQLAlchemy; **MongoDB** optional), exports a **JSON audit trail**, optionally resolves the **vehicle owner** from a registry, and **notifies** the owner with fine and location context.

The mobile application provides **live capture**, **gallery-based testing**, **vehicle owner registration**, **violation lists**, **evidence viewing**, and **analytics dashboards** fed by aggregated API endpoints (daily, weekly, monthly). The architecture separates **inference**, **business logic**, and **presentation**, enabling deployment on edge servers or cloud hosts close to cameras.

**Keywords:** Helmet violation detection, YOLOv8, ANPR, EasyOCR, PaddleOCR, Flask, Flutter, smart mobility, traffic enforcement, notifications, SQLite, MongoDB.

---

## Table of Contents

| Section | Title | Page |
|--------|--------|------|
| | Title Page | i |
| | Certificate | ii |
| | Declaration | iii |
| | Acknowledgement | iv |
| | Abstract | v |
| | Table of Contents | vi |
| | List of Figures | vii |
| **1** | **Introduction** | **1** |
| 1.1 | Introduction | 1 |
| 1.2 | Problem Statement | 1 |
| 1.3 | Motivation | 2 |
| 1.4 | Objectives | 3 |
| 1.5 | Scope of the Project | 3 |
| 1.6 | Organization of the Report | 3 |
| **2** | **Literature Survey** | **4** |
| 2.1 | Related Work | 4 |
| 2.1.1 | Traditional Traffic Enforcement Challenges | 4 |
| 2.1.2 | Artificial Intelligence in Road Safety | 4 |
| 2.1.3 | Helmet and Rider Detection Using Deep Learning | 4 |
| 2.1.4 | Object Detection Architectures and YOLO Family | 4 |
| 2.1.5 | License Plate Localization and OCR | 5 |
| 2.1.6 | Automatic Number Plate Recognition Pipelines | 5 |
| 2.1.7 | Smart City and Intelligent Transportation Systems | 5 |
| 2.1.8 | Integrated Violation Management and Citizen Notifications | 5 |
| **3** | **Proposed System** | **6** |
| 3.1 | Existing System | 6 |
| 3.2 | Proposed System | 6 |
| 3.2.1 | Helmet Detection Using YOLO and Class-Aware Logic | 7 |
| 3.2.2 | Bounding-Box Guided Plate Region Extraction | 7 |
| 3.2.3 | OCR Engines and Semantic Validation of Plate Text | 7 |
| 3.2.4 | Violation Decision Policy and Evidence Capture | 8 |
| 3.2.5 | Owner Registry Lookup and Fine Assignment | 8 |
| 3.2.6 | Notification Channels and Analytics Aggregation | 8 |
| 3.3 | Methodology | 9–10 |
| 3.4 | Algorithms Used | 10–15 |
| 3.5 | System Requirements | 15 |
| 3.5.1 | Hardware Requirements | 15 |
| 3.5.2 | Software Requirements | 15 |
| **4** | **System Design** | **16** |
| 4.1 | Overview | 17 |
| 4.2 | System Design | 18 |
| 4.2.1 | Class Diagram | 18 |
| 4.2.2 | Use Case Diagram | 19 |
| 4.2.3 | Sequence Diagram | 20 |
| 4.2.4 | Data Flow Diagram | 21 |
| 4.3 | Modules Used | 23 |
| 4.3.1 | API and Configuration Module | 23 |
| 4.3.2 | Image Ingestion and Pre-Processing Module | 23 |
| 4.3.3 | Helmet Detection Module | 23 |
| 4.3.4 | ANPR Module | 23 |
| 4.3.5 | Violation Persistence Module | 24 |
| 4.3.6 | Vehicle Registry Module | 24 |
| 4.3.7 | Notification Module | 24 |
| 4.3.8 | Analytics Module | 24 |
| **5** | **Implementation and Testing** | **25** |
| 5.1 | Application Initialization | 25 |
| 5.1.1 | Client Configuration and API Base URL | 25 |
| 5.1.2 | Capture, Upload, and Detection Request | 26 |
| 5.1.3 | Vehicle Owner Registration | 27 |
| 5.1.4 | Violation Listing and Evidence Retrieval | 27 |
| 5.1.5 | Video Stream Integration | 28 |
| 5.1.6 | Analytics Dashboards | 28 |
| 5.2 | Technology Stack | 29 |
| **6** | **Conclusion and Future Enhancement** | **30** |
| 6.1 | Conclusion | 30 |
| 6.2 | Future Enhancement | 30 |
| 6.2.1 | Integration of Advanced AI Models | 30 |
| 6.2.2 | Integration with Transport Department Systems | 31 |
| 6.2.3 | Cloud-Based Deployment and Edge Optimization | 32 |
| **7** | **References** | **33** |

*(Page numbers are indicative; renumber after inserting figures and institution forms.)*

---

## List of Figures

| Fig. | Description |
|------|-------------|
| Fig. 4.1 | High-level system architecture (cameras, API, mobile app, database) |
| Fig. 4.2 | Class diagram—services and persistence layer |
| Fig. 4.3 | Use case diagram—enforcement officer and system |
| Fig. 4.4 | Sequence diagram—`/api/detect` violation path |
| Fig. 4.5 | Data flow diagram—level 0 / level 1 |
| Fig. 5.1 | Mobile capture and multipart upload flow |
| Fig. 5.2 | Sample annotated violation evidence image |

---

# 1 Introduction

## 1.1 Introduction

Motorized two-wheelers are a dominant mode of transport in many regions due to flexibility, lower cost, and maneuverability in congestion. However, they are also disproportionately involved in fatal and serious injuries, with **head trauma** being a leading cause of death when riders omit protective helmets. Statutes in numerous jurisdictions mandate helmet use, yet **compliance varies** with visibility of enforcement, public awareness, and practicality of detection at scale.

**Computer vision** and **multimodal sensing** offer a pathway to augment human patrols: cameras at junctions, toll plazas, and campus gates can capture high-resolution frames, while modern **deep learning detectors** can localize riders and classify helmet use faster than manual review. Coupling detection with **automatic number plate recognition** allows associations between **visual evidence**, **vehicle identity**, and **registered owner data**, enabling **automated challans** (fines) and **timely notifications**.

This project implements an end-to-end **Helmet Violation Detection and Notification System**. A **Python Flask** server exposes endpoints for **health checks**, **image-based detection**, **violation retrieval**, **owner registration and lookup**, **manual notification triggers**, and **analytics**. A **Flutter** application provides an operational dashboard for field trials: **camera capture**, **optional manual plate override**, **violation history**, and **charts**. Optional scripts process **live video** by forwarding frames to the API.

The design emphasizes **evidence integrity** (saved annotated frames), **operational safety** (avoiding false violations when helmet models are unavailable), and **integration points** (database backends, messaging APIs, JSON export).

## 1.2 Problem Statement

Despite legal mandates, **helmet non-compliance** persists because:

1. **Enforcement is sparse** relative to road length and trip volume.  
2. **Human officers** cannot monitor all approaches simultaneously; fatigue and distraction affect consistency.  
3. **Post-hoc identification** of violators is difficult without **plate-level identity** tied to **evidence**.  
4. **Notification latency** reduces deterrence; timely communication increases perceived enforcement.  
5. **Data fragmentation**—images on one device, registers in another spreadsheet, fines on paper—**blocks analytics** and audit.

The core problem this project addresses is: **How to automatically detect two-wheeler riders without helmets from camera images, reliably read or associate a vehicle registration number, persist a tamper-evident record, and notify stakeholders—while providing analytics for planners—all within a maintainable software architecture.**

Constraints include **variable illumination**, **occlusion**, **angular plate visibility**, **OCR errors**, **model availability** on deployment hardware, and **privacy** considerations around imaging in public space.

## 1.3 Motivation

**Public health and safety** motivations are paramount: helmets reduce traumatic brain injury risk. From an engineering standpoint, the project is motivated by:

- **Scalability:** The same API can serve many camera ingress points.  
- **Reproducibility:** Open components (Flask, Ultralytics, OpenCV) lower vendor lock-in.  
- **Education:** The stack demonstrates the full ML operations path—**data in**, **model inference**, **post-processing**, **storage**, and **UI**.  
- **Citizen services:** Automated SMS/WhatsApp messages can include **fine amounts** and **payment references**, improving transparency if integrated with payment gateways.  
- **Policy feedback:** Aggregated analytics highlight **hotspots** and **temporal trends**.

The repository’s implementation choices—**conservative violation gating** when only generic object detectors are present, **EXIF-aware image loading** for mobile photos, and **dual OCR backends**—reflect practical deployment lessons where **false positives** erode trust and **brittle OCR** blocks downstream automation.

## 1.4 Objectives

The primary objectives are:

1. **Detect helmet violations** from static images using a **YOLOv8**-compatible pipeline, distinguishing *helmet present* vs *helmet absent* when class definitions permit.  
2. **Extract and normalize** Indian-style **license plates** using **PaddleOCR/EasyOCR** with **regex validation**.  
3. **Persist violations** with **metadata** (timestamp, location, fine, status, owner fields when known) in **SQLite** (default) or **MongoDB**, and mirror records to **JSON** export.  
4. **Notify** registered owners via **Twilio** SMS and/or WhatsApp when phone numbers exist.  
5. Deliver a **Flutter** client for **capture**, **history**, **owner onboarding**, **settings**, and **analytics**.  
6. Provide **HTTP analytics endpoints** for time-bucketed counts (daily, weekly, monthly) and summary statistics.  
7. Support **optional video stream processing** by posting frames to the API with location context.

## 1.5 Scope of the Project

**In scope:**

- Server-side **single-frame inference** and client-side **image upload**.  
- **Registry** of vehicle owners and **lookup** by plate.  
- **Violation CRUD** at list/get granularity; **image retrieval** for evidence.  
- **Notification** stubs integrated with Twilio configuration.  
- **Analytics** derived from stored violation timestamps.  

**Out of scope / assumptions:**

- Full **court-grade forensic** chain-of-custody and digital signing of media.  
- Real-time **multi-object tracking** across long video without identity handover (the provided `video_processor` posts frames; tracking IDs are not modeled).  
- Native **payment gateway** settlement; links may be referenced in templates but end-to-end payments are external.  
- **Multi-tenant** RBAC for large organizations (the mobile app uses configurable API URL without embedded login in the base codebase).  
- **Calibration** of cameras for speed or red-light combined offenses.

## 1.6 Organization of the Report

- **Chapter 2** surveys related literature on enforcement bottlenecks, AI in road safety, detection models, and ANPR.  
- **Chapter 3** presents the **proposed system**, methodology, algorithmic outline, and requirements.  
- **Chapter 4** details **system design**, architectural views, and module decomposition aligned with the codebase.  
- **Chapter 5** describes **implementation** and a **testing** narrative.  
- **Chapter 6** concludes and proposes **future enhancements**.  
- **Chapter 7** lists **references**.

---

# 2 Literature Survey

## 2.1 Related Work

### 2.1.1 Traditional Traffic Enforcement Challenges

Traditional enforcement relies on **visible patrols** and **manual evidence collection**. Challenges include **non-stationary violators**, **disputes over identity**, **inconsistent fine application**, and **limited nighttime coverage**. Manual plate transcription introduces **errors**, and paper registers complicate **longitudinal analysis**. These factors motivate **sensor-backed automation** with **digitized audit logs**.

### 2.1.2 Artificial Intelligence in Road Safety

AI methods now support **incident prediction**, **traffic state estimation**, **dangerous maneuver detection**, and **vulnerable road user protection**. Convolutional and transformer-backed architectures process **RGB frames** and, where available, **LiDAR** or **IR**. For helmet compliance, supervised detectors trained on curated rider datasets outperform classical **hand-crafted features** in cluttered scenes.

### 2.1.3 Helmet and Rider Detection Using Deep Learning

Helmet classification is often framed as **object detection** (person, head, helmet) or **fine-grained classification** on cropped head regions. Datasets vary by **camera angle**, **helmet diversity**, and **pillion passengers**. Handling **occluded faces**, **reflections**, and **similar color confusion** (caps vs helmets) remains active research. Practical systems combine **detector confidence thresholds** with **temporal smoothing** when video is available.

### 2.1.4 Object Detection Architectures and YOLO Family

The **YOLO** (“You Only Look Once”) family performs **single-pass** grid-based detection with favorable **latency-accuracy** tradeoffs for surveillance. **YOLOv8** (Ultralytics) improves training workflows and export paths. In deployment, **model quantization** and **TensorRT/ONNX** runtimes can reduce latency, though this project uses **PyTorch** inference via Ultralytics for clarity.

### 2.1.5 License Plate Localization and OCR

Plates differ by **country layout** and **font**. Indian plates often follow **state code + district + series + number** with variable spacing. Localization strategies include **morphological operations**, **edge maps**, **character segmentation**, or leveraging **detector proposals**. Deep-learning detectors can learn plate bounding boxes jointly with vehicles.

### 2.1.6 Automatic Number Plate Recognition Pipelines

End-to-end ANPR chains: **acquisition → optional stabilization → localization → perspective correction → OCR → lexicon/pattern validation → checksum**. Engines such as **EasyOCR** and **PaddleOCR** provide ready readers; domain adaptation improves accuracy on local fonts. Post-OCR **regex filtering** removes low-confidence gibberish.

### 2.1.7 Smart City and Intelligent Transportation Systems

Municipal **ITS** stacks integrate **cameras**, **edge compute**, **centralized dashboards**, and **open data APIs**. Privacy-by-design considerations include **data minimization**, **retention policies**, and **masking** non-involved pedestrians when feasible.

### 2.1.8 Integrated Violation Management and Citizen Notifications

Modern stacks unify **detection events**, **billing systems**, and **SMS gateways**. Template messages via **WhatsApp Business** APIs require provider approval. Twilio abstracts **SMS/MMS/WhatsApp** with consistent REST patterns, suitable for prototypes bridging to production notification hubs.

---

# 3 Proposed System

## 3.1 Existing System

Conventional setups include **CCTV recording** with **manual review**, **roadside checkpoints**, or **standalone speed guns** without helmet classification. **Disadvantages:** high labor cost, **subjective judgment**, **weak metadata linkage**, and **delayed reporting**. Some cities pilot **ANPR** for tolling but omit **helmet-specific** models. Spreadsheets for fines are **error-prone** and do not scale.

## 3.2 Proposed System

The proposed system is a **unified detection-service-mobile stack**:

- **Ingress:** Multipart **JPEG/PNG** uploads from **Flutter** or automated **video_processor** scripts.  
- **Vision:** **HelmetDetector** runs YOLO; violations arise from **without-helmet** class predictions above a **confidence threshold**.  
- **Identity:** **ANPR** reads plates, normalized via `normalize_for_storage`.  
- **Persistence:** SQLAlchemy **Violation** rows (SQLite default) or Mongo collections; **JSON export** mirrors inserts.  
- **Engagement:** **NotificationService** sends alerts when owner phone numbers exist.  
- **Insight:** **AnalyticsService** aggregates counts for charts.

### 3.2.1 Helmet Detection Using YOLO and Class-Aware Logic

The `HelmetDetector` resolves **class indices** from model `names` (*with* vs *without* helmet synonyms). If a dedicated helmet model path or Hugging Face artifact loads successfully, **without-helmet** boxes trigger violations. If unavailable, a **COCO** pretrained **YOLOv8n** may load but **does not** flag helmet violations (by design) to **avoid false positives** from generic person/bike classes.

### 3.2.2 Bounding-Box Guided Plate Region Extraction

Given the best rider/head bounding box, `ANPR.extract_plate_region` crops a **vertically extended window** under the detection to include likely plate locations across angles, with horizontal padding. Full-frame OCR runs as **fallback** if plate remains unknown.

### 3.2.3 OCR Engines and Semantic Validation of Plate Text

**PaddleOCR** is preferred when installed; otherwise **EasyOCR** lazy-loads with retries around file-lock issues on Windows. Recognized strings pass through **uppercasing**, **spacing normalization**, and **pattern checks** (`PLATE_PATTERN`, rejection of all-letter junk).

### 3.2.4 Violation Decision Policy and Evidence Capture

On **without-helmet** detections, the server writes **`violation_<plate>_<timestamp>.jpg`** under the configured violations folder after drawing **visual annotations** (`draw_helmet_status`). Records include **camera_location**, **fine_amount** (code default, e.g., 400 currency units), and **pending** status.

### 3.2.5 Owner Registry Lookup and Fine Assignment

`VehicleRegistry` maps normalized plates to **owner_name**, **phone_number**, **address** where registered. Lookup informs whether notifications can fire automatically. Fine amounts may be centralized in configuration or expanded per offense class in future iterations.

### 3.2.6 Notification Channels and Analytics Aggregation

Twilio-backed **SMS** and **WhatsApp** functions compose concise violation summaries with **location** and **fine**. Analytics endpoints return **daily buckets**, **weekly comparisons**, and **monthly trends** for dashboards.

## 3.3 Methodology

**Requirements analysis:** Define actors (operator, system, vehicle owner), data artifacts (image, plate, violation row), and non-functional needs (latency targets, storage growth).

**Model acquisition:** Obtain a **helmet-aware YOLO** weight file or rely on download helpers; validate class naming conventions. Document fallback behavior explicitly for auditors.

**API-first design:** Specify **`/api/detect`** contract: multipart field **`image`**, optional **`camera_location`**, optional **`vehicle_number`** override for low-OCR conditions during testing.

**Incremental testing:**  
- **Unit-style:** Regex acceptance on synthetic OCR strings.  
- **Integration:** Postman/cURL uploads; verify DB rows and files.  
- **Field:** Mobile capture under sun/shade; measure OCR success vs crop quality.

**Deployment rehearsal:** Configure `.env` for **Twilio** and optional **MongoDB**; run `init_db` script; set Flutter base URL for emulator (`10.0.2.2`) vs LAN IP for devices.

**Ethics & privacy:** Retain images only as needed; inform stakeholders of monitoring; restrict API exposure with network controls in production.

## 3.4 Algorithms Used

**3.4.1 YOLO Inference Loop**  
For each input frame tensor, the model predicts **bounding boxes**, **class probabilities**, and **objectness**. Conventional **NMS** suppresses overlapping predictions. Thresholding (e.g., **0.25** confidence in API calls) filters low-quality boxes. For helmet models, select boxes where `class_id == without_helmet_index`.

**3.4.2 Class Index Resolution**  
Iterate `model.names`; map textual labels containing *without*, *no_helmet* variants to violation class; map *with* helmet labels excluding negation patterns to compliant class. This **string heuristic** adapts to community-trained checkpoints without hard-coded IDs.

**3.4.3 Helmet Status Aggregation**  
`detect_helmet_status` combines counts of **with** and **without** detections, computes **`helmet_present`** booleans, and selects **`best_bbox`** for ANPR cropping—typically prioritizing high-confidence **without** boxes, else strong **with** boxes, depending on implementation details in `helmet_detector.py`.

**3.4.4 Plate Region Cropping**  
Given `[x1,y1,x2,y2]`, expand vertically **downward** (positive image y) to capture plates often below the rider’s head region; clamp to frame bounds; add symmetric horizontal padding.

**3.4.5 OCR Decoding**  
Reader modules output **character sequences** with confidences. Post-process: remove illegal characters, merge tokens, compare against **Indian plate regexes**; accept first high-confidence match or return `UNKNOWN` when none qualify.

**3.4.6 Image Orientation Correction**  
`PIL.ImageOps.exif_transpose` corrects phone camera rotation before array conversion and **BGR** color ordering for OpenCV compatibility—reducing **sideways plates** that confuse OCR.

**3.4.7 Persistence Algorithm**  
SQLAlchemy path: open session → instantiate **Violation** ORM object → `commit()` → close session. Mirror serialized dict to JSON with ISO-8601 timestamps for interoperability.

**3.4.8 Notification Dispatch**  
Construct templated message bodies including **vehicle_number**, **fine_amount**, **camera_location**; invoke Twilio REST wrappers; capture per-channel success flags in response payload for UI/logs.

## 3.5 System Requirements

### 3.5.1 Hardware Requirements

| Role | Minimum | Recommended |
|------|---------|---------------|
| Inference server | 4 CPU cores, 8 GB RAM | NVIDIA GPU (6+ GB VRAM), 16+ GB RAM |
| Storage | 10 GB free | SSD; larger volume for footage/evidence retention |
| Network | Stable LAN/WAN for Twilio | Low-latency uplink from cameras to server |
| Mobile client | Mid-range Android/iOS | Device with quality camera and API reachability |

### 3.5.2 Software Requirements

| Component | Version / Notes |
|-----------|-----------------|
| Python | 3.10+ (3.12 supported per requirements pin strategy) |
| Flask, flask-cors | REST API |
| PyTorch, torchvision, ultralytics | YOLO inference |
| OpenCV, Pillow | Image I/O and drawing |
| EasyOCR / PaddleOCR | ANPR |
| SQLAlchemy | ORM for SQLite/MySQL paths |
| pymongo | Optional MongoDB |
| Twilio SDK | SMS/WhatsApp |
| Flutter SDK | Mobile build toolchain |

---

# 4 System Design

## 4.1 Overview

Architecturally, the system follows **three tiers**:

1. **Acquisition tier:** Cameras or mobile sensors produce RGB frames.  
2. **Processing tier:** Flask coordinates **HelmetDetector**, **ANPR**, **registry**, **notifications**, and **analytics**.  
3. **Presentation tier:** Flutter screens consume JSON, render charts, and manage settings.

Cross-cutting concerns include **logging**, **CORS** for local dev, **maximum upload size** limits, and **directory provisioning** for uploads/violations/export paths.

## 4.2 System Design

### 4.2.1 Class Diagram (Conceptual)

Key classes and services:

- **`HelmetDetector`:** `detect_violations`, `detect_helmet_status`, `draw_clhelmet_status`, internal `_detect_with_helmet_model`.  
- **`ANPR`:** `read_plate`, `extract_plate_region`, lazy OCR reader getters.  
- **`VehicleRegistry`:** `lookup_owner`, `register_owner`.  
- **`NotificationService`:** `send_sms`, `send_whatsapp`, `send_both`.  
- **`AnalyticsService`:** `get_daily_violations`, `get_weekly_comparison`, `get_monthly_trends`, `get_summary`.  
- **ORM `Violation`, `VehicleOwner`:** persistence entities with `to_dict` helpers.

Associations: Flask **`app`** aggregates singleton service instances; `_save_violation_db` bridges services to storage.

### 4.2.2 Use Case Diagram (Narrative)

**Actors:** *Traffic Operator*, *System Administrator*, *Registered Vehicle Owner*, *External SMS Gateway*.

**Use cases:** Configure API URL; Capture image; Upload for detection; Register owner; Lookup owner; View violation list; Open evidence image; Receive SMS/WhatsApp alert; Query analytics summaries; Switch database backend via environment.

### 4.2.3 Sequence Diagram (Violation Path)

1. Client `POST /api/detect` with **multipart image**.  
2. Server loads image, fixes EXIF orientation, converts color space.  
3. `HelmetDetector.detect_helmet_status`.  
4. If violations empty → return JSON with **helmet** metadata and plate OCR result.  
5. If violations present → annotate frame, write JPEG, `VehicleRegistry.lookup_owner`, `_save_violation_db`, optional `NotificationService.send_both`, return enriched JSON.

### 4.2.4 Data Flow Diagram

**Level 0:** External world → **Helmet System** → Owners/Administrators.

**Level 1 processes:** Image ingest → Detection → OCR → Violation decision → Storage → Notification → Analytics queries → Mobile views.

**Data stores:** Violations table/collection; evidence files; JSON exports; optional owner table.

## 4.3 Modules Used

### 4.3.1 API and Configuration Module

`app.py` defines routes; `config.settings` centralizes paths, DB type, keys.**`before_request` logging** aids traceability.

### 4.3.2 Image Ingestion and Pre-Processing Module

Multipart parser, **PIL** loading, **EXIF** transpose, **numpy** array bridging, **OpenCV** color conversion.

### 4.3.3 Helmet Detection Module

Encapsulates YOLO lifecycle and class-aware logic; draws overlays for auditing.

### 4.3.4 ANPR Module

Wraps OCR engines, heuristics for Indian plates, cropping relative to detections.

### 4.3.5 Violation Persistence Module

ORM insert paths, Mongo fallback, JSON mirror for ETL integrations.

### 4.3.6 Vehicle Registry Module

Owner lifecycle: register & lookup for downstream messaging.

### 4.3.7 Notification Module

Abstracts Twilio interactions, templated messaging, dual-channel orchestration.

### 4.3.8 Analytics Module

Time-series aggregations powering mobile charts and reporting endpoints.

---

# 5 Implementation and Testing

## 5.1 Application Initialization

Backend entry initializes Flask, ensures directories, constructs service singletons, and calls `init_mysql()` for SQLite/MySQL modes. Mobile `main.dart` wires **Provider** for `ApiService` and `RefreshNotifier`, sets **Material 3** theme, and mounts `HomeScreen`.

### 5.1.1 Client Configuration and API Base URL

`ApiService` exposes `setBaseUrl`; **Settings** screen persists operator-supplied host—critical because Android emulators cannot reach `localhost` on the host directly (`10.0.2.2` alias used). Physical devices require **LAN IP** and firewall allowances on port **5000**.

### 5.1.2 Capture, Upload, and Detection Request

`camera_screen.dart` captures photos via **camera** plugin, optionally reads manual plate text, sends multipart POST through `detectViolation`. UI binds **helmet_present**, **vehicle_number**, and violation dialogs. Gallery pick path supports offline stills for regression demos.

### 5.1.3 Vehicle Owner Registration

`add_vehicle_screen.dart` collects owner identity fields, posts JSON to `/api/owner/register`, aligning with normalization routines shared client-side (`normalizePlate`).

### 5.1.4 Violation Listing and Evidence Retrieval

`violations_screen.dart` lists historical entries; API pagination parameters (`limit`, `offset`) throttle payload size. Image endpoint `/api/violations/<id>/image` serves static JPEG evidence when paths resolve on server disk.

### 5.1.5 Video Stream Integration

`video_processor.py` (repository utility) loops over a video capture device or stream URL, encodes frames, and posts them—simulating fixed-camera deployments. Operators label **`camera_location`** consistently for analytics.

### 5.1.6 Analytics Dashboards

`analytics_screen.dart` queries `/api/analytics/daily|weekly|monthly` and summary routes, rendering charts consistent with theme colors. Useful for demonstrating **trend reduction** after awareness campaigns.

### Testing Notes

- **Happy path:** Upload frame with obvious plate → expect structured JSON, DB row when violating.  
- **Negative path:** Helmet present → `violation_detected: false`, no evidence file growth.  
- **OCR stress:** Motion blur frames → expect `UNKNOWN` plate with optional manual override field.  
- **Service mocks:** Twilio can be disabled in dev to avoid charges; verify guard clauses/logging.

## 5.2 Technology Stack

| Layer | Technology |
|-------|------------|
| API framework | Flask 3, flask-cors |
| Vision | OpenCV, Ultralytics YOLOv8, PyTorch |
| OCR | EasyOCR, optional PaddleOCR |
| DB | SQLite + SQLAlchemy (default), MongoDB optional |
| Messaging | Twilio |
| Mobile | Flutter (Material 3), Provider, http multipart client |
| Tooling | python-dotenv, huggingface-hub for model artifacts |

---

# 6 Conclusion and Future Enhancement

## 6.1 Conclusion

This project delivers a **practical, modular helmet violation stack** bridging **state-of-the-art object detection** with **ANPR**, **structured persistence**, and **actionable notifications**. The Flask API’s clear REST surface enables diverse clients beyond the shipped Flutter application, while conservative fallback behavior acknowledges **real-world model availability** constraints. Evidence capture and JSON mirroring strengthen **auditability**. Analytics endpoints transform raw detections into **management insights**.

Educationally, the work spans the full pipeline from **sensor data** to **user-facing dashboards**, illustrating how **ML components** must coexist with **software engineering** discipline—validation, storage schemas, operational logging, and configuration management.

## 6.2 Future Enhancement

### 6.2.1 Integration of Advanced AI Models

- Adopt **higher-capacity** YOLO variants or **transformer detectors** where GPUs allow.  
- Employ **temporal smoothing** and **multi-frame reasoning** to reduce flicker false alarms.  
- Explore **on-device** TFLite/ONNX models on the phone for **offline triage**.

### 6.2.2 Integration with Transport Department Systems

- Bi-directional sync with **official vehicle registries** and **challan payment portals**.  
- Digital signatures on evidence packages; **blockchain anchoring** optional for integrity marketing.

### 6.2.3 Cloud-Based Deployment and Edge Optimization

- Containerize API with **GPU-aware** Kubernetes manifests; place **lightweight edge boxes** at cameras for preprocessing.  
- Implement **auto-scaling** ingestion queues (Kafka/RabbitMQ) during peak hours.  
- Add **role-based auth**, **rate limiting**, and **TLS termination** at load balancers for public-sector readiness.

---

# 7 References

1. Jocher, G., et al. **Ultralytics YOLOv8** documentation and repository (object detection framework).  
2. Redmon, J., et al. **You Only Look Once: Unified, Real-Time Object Detection.** CVPR 2016. (Historical YOLO lineage.)  
3. OpenCV Team. **OpenCV Library Documentation** — image processing and visualization.  
4. EasyOCR Project. **EasyOCR** — deep learning OCR toolkit.  
5. PaddlePaddle Authors. **PaddleOCR** — practical OCR system.  
6. Flask Development Team. **Flask Web Framework Documentation.**  
7. Google Flutter Team. **Flutter Documentation** — cross-platform UI toolkit.  
8. SQLAlchemy Authors. **SQLAlchemy ORM Documentation.**  
9. MongoDB Inc. **MongoDB Manual** — NoSQL document database.  
10. Twilio Inc. **Twilio API Documentation** — programmable SMS & WhatsApp.  
11. World Health Organization. **Road Traffic Injury Prevention** materials — public health rationale for helmets.  
12. Regional Motor Vehicle Act regulations — legal context for helmet mandates and penalties (cite specific local statute in final submission).  
13. Goodfellow, I., Bengio, Y., Courville, A. *Deep Learning.* MIT Press, 2016 — foundations for CNN detectors.  
14. Stallings, W. *Computer Security: Principles and Practice* — themes on data retention and system hardening.  
15. Newcombe, C., et al. *Formal Verification at AWS* — inspiration for high-assurance production lessons (operational rigor).

---

# Appendices (Optional for Printed Report)

**Appendix A — API Endpoint Summary**

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/health` | Liveness |
| POST | `/api/detect` | Image inference |
| GET | `/api/violations` | List violations |
| GET | `/api/violations/<id>` | Detail |
| GET | `/api/violations/<id>/image` | Evidence JPEG |
| GET | `/api/owner/lookup` | Registry query |
| POST | `/api/owner/register` | Registry insert |
| POST | `/api/notify` | Manual notify |
| GET | `/api/analytics/*` | Aggregations |

**Appendix B — Environment Variables (Indicative)**  
`DATABASE_TYPE`, `MONGODB_URI`, `TWILIO_*`, `HELMET_MODEL_PATH`, upload paths — consult `backend/.env.example` if present in deployment.

**Appendix C — Ethics Checklist**  
Public signage, retention schedule, access control on evidence exports, DPIA where applicable.

---
*End of report body.*
