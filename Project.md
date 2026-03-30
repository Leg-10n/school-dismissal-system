# Smart School Dismissal System – SaaS MVP Specification

---

# IMPORTANT DEVELOPMENT RULE

This project must be built phase-by-phase.

DO NOT attempt to build the entire system at once.

At the start of every phase:

1 Provide implementation plan
2 List files to create
3 List dependencies
4 Identify risks
5 Then implement

Never skip planning.

---

# AI ENGINEERING ROLE

You are a senior full-stack software engineer assisting me in building this SaaS MVP.

You must act as:

• Software Architect  
• Backend Engineer  
• Frontend Engineer  
• Mobile Engineer  
• QA Engineer  
• DevOps Engineer  

You must think like a senior startup engineer, not a tutorial assistant.

Your job is to help build a convincing SaaS MVP using proper engineering practices.

---

# ENGINEERING MINDSET REQUIREMENTS

You must:

Plan before coding.

Build in small iterations.

Keep architecture clean.

Avoid hacks unless marked MVP shortcut.

Use best practices of the language and frameworks.

Follow SOLID principles when reasonable.

Prefer readable code over clever code.

Use consistent naming.

Avoid technical debt.

Refactor when needed.

Think before implementing.

---

# COMMUNICATION STYLE

Be concise.

Be technical.

Avoid filler text.

Explain only important decisions.

Focus on implementation quality.

Act like a senior engineer reviewing a junior developer’s work.

---

# PROJECT GOAL

Build a Smart School Pickup Management System that demonstrates:

1 Automatic parent arrival detection (camera plate recognition)

2 Manual parent arrival via mobile app

3 Real time pickup dashboard for school staff

4 Parent pickup status notifications

5 Safe pickup workflow tracking

The MVP must demonstrate a complete dismissal workflow.

Arrival → Queue → Release → Pickup → Confirmation

---

# CORE WORKFLOW MODEL

Student pickup lifecycle:

WAITING  
ARRIVED  
SENT_TO_GATE  
PICKED_UP  

Transitions:

WAITING → ARRIVED  
Triggered by:
Camera detection OR parent app

ARRIVED → SENT_TO_GATE  
Triggered by teacher

SENT_TO_GATE → PICKED_UP  
Triggered by teacher

Invalid transitions must be prevented.

---

# SYSTEM ARCHITECTURE

High Level Design:

CAMERA SERVICE (Python ANPR)
        ↓
FASTAPI BACKEND
        ↓
--------------------------------
↓                              ↓
SCHOOL DASHBOARD          PARENT MOBILE APP
React Web                React Native Expo

Communication:

REST → Commands

WebSocket → Realtime updates

---

# TECH STACK

Backend:

FastAPI  
PostgreSQL  
SQLAlchemy  
Pydantic  
WebSockets  
Uvicorn  

Frontend Dashboard:

React
Vite
TailwindCSS
WebSocket client

Parent App:

React Native
Expo

Camera Service:

Python
OpenCV
Plate Recognition library
Requests

Testing:

pytest
React Testing Library (optional)

Environment:

Local development.

Docker optional.

---

# MVP DESIGN CONSTRAINTS

Allowed shortcuts:

No authentication

Single school

Local deployment

Simulated notifications

No billing

Not allowed shortcuts:

Messy architecture

No tests

Hardcoded logic

No error handling

Bad structure

---

# DATABASE DESIGN

## students

id (UUID primary key)

name (string)

grade (string)

status (enum)

pickup_person (string)

created_at

updated_at

status values:

WAITING

ARRIVED

SENT_TO_GATE

PICKED_UP

---

## parents

id

name

phone

email

created_at

---

## cars

id

plate_number (unique indexed)

parent_id

student_id

created_at

---

## pickup_events

id

student_id

event_type

source

timestamp

notes

event_type:

ARRIVED

SENT

PICKED

source:

CAMERA

APP

MANUAL

---

# BACKEND FEATURE SET

Student Service:

Create student

List students

Update student

Reset daily status

API:

GET /students

POST /students

PATCH /students/{id}

POST /students/reset

---

Car Service:

Register vehicles.

POST /cars

GET /cars

---

Detection Service:

POST /detect

Input:

plate_number

confidence

Logic:

Normalize plate.

Find car.

Find student.

If status WAITING:

Change → ARRIVED.

Create pickup event.

Broadcast websocket.

If unknown:

Log detection.

Return UNKNOWN.

Must include cooldown logic.

---

Parent Arrival Service:

POST /arrival

Logic:

WAITING → ARRIVED.

Source APP.

Broadcast update.

Prevent duplicate arrivals.

---

Pickup Workflow:

POST /students/{id}/send

ARRIVED → SENT_TO_GATE.

POST /students/{id}/pickup

SENT_TO_GATE → PICKED_UP.

Create events.

Broadcast updates.

Trigger parent notification.

---

# REALTIME SYSTEM

WebSocket endpoint:

/ws

Events:

student_updated

Payload:

student_id

name

status

source

timestamp

All clients subscribe:

Dashboard

Parent App

---

# SCHOOL DASHBOARD FEATURES

Main Board:

Columns:

WAITING

ARRIVED

SENT_TO_GATE

PICKED_UP

Students move live.

Kanban layout preferred.

---

Student Card:

Show:

Name

Grade

Arrival source

Arrival time

Buttons:

SEND TO GATE

MARK PICKED UP

---

Detection Feed:

Recent detections:

ABC1234 → Emma

XYZ111 → UNKNOWN

---

Admin Controls:

RESET DAY button.

Resets all students to WAITING.

---

# PARENT MOBILE APP FEATURES

Home Screen:

Show:

Student name

Grade

Pickup status

Button:

I AM HERE

---

Status Messaging:

WAITING:

Waiting for pickup.

ARRIVED:

Parent detected.
Waiting for teacher release.

SENT:

Student coming to pickup area.

PICKED:

Student picked up successfully.

---

Parent Actions:

I AM HERE:

Triggers arrival.

My Cars:

Add plate.

List plates.

---

Notifications:

Use WebSocket first.

Push notifications later.

---

# CAMERA SERVICE

Flow:

Start webcam.

Capture frame.

Run plate recognition.

Extract text.

If confidence high:

Send POST /detect.

Cooldown:

Prevent duplicate send within 10 seconds.

Console logs:

Detected plate.

Matched student.

Unknown vehicle.

---

# FOLDER STRUCTURE

Backend:

backend/

app/

main.py

models.py

schemas.py

database.py

config.py

routers/

students.py

cars.py

detection.py

pickup.py

services/

student_service.py

detection_service.py

pickup_service.py

websocket/

manager.py

tests/

test_students.py

test_detection.py

---

Dashboard:

dashboard/

pages/

Dashboard.jsx

components/

StudentColumn.jsx

StudentCard.jsx

DetectionFeed.jsx

services/

api.js

socket.js

---

Parent App:

parent-app/

screens/

HomeScreen

StatusScreen

CarsScreen

services/

api.js

socket.js

components/

StatusBadge

StudentCard

---

Camera:

camera/

detect.py

plate_reader.py

api_client.py

---

# CODE QUALITY RULES

Always:

Separate routers/services/models.

Validate inputs.

Handle errors.

Use environment variables.

Use reusable functions.

Avoid duplication.

Never mix business logic into routers.

---

# DATABASE RULES

Use UUIDs.

Use timestamps.

Use enums.

Index plates.

Avoid nullable unless necessary.

---

# API RULES

Use REST naming.

Return proper HTTP codes.

200 success

400 validation

404 missing

500 error

Return useful error messages.

---

# TESTING REQUIREMENTS

Backend must include:

Unit tests.

API tests.

Edge case tests.

Failure tests.

Use pytest.

Test:

Valid transitions.

Invalid transitions.

Duplicate arrival.

Unknown plates.

Invalid IDs.

---

# EDGE CASES

Must handle:

Duplicate detection.

Student already arrived.

Unknown plate.

Parent presses twice.

Teacher sends twice.

Pickup without arrival.

WebSocket disconnect.

Race conditions.

---

# LOGGING REQUIREMENTS

Backend must log:

Detections.

Arrival events.

Pickup events.

Unknown vehicles.

Errors.

Use Python logging.

---

# BUILD EXECUTION PLAN

Follow strictly.

---

PHASE 1 Backend Foundation:

Setup FastAPI.

Setup database.

Create models.

Create config.

Health endpoint.

Tests:

API boots.

Tables exist.

DB connects.

---

PHASE 2 Core Workflow:

Student CRUD.

Status transitions.

Arrival logic.

Pickup logic.

Tests:

Lifecycle works.

Invalid transitions blocked.

---

PHASE 3 Realtime:

WebSocket manager.

Connection tracking.

Broadcast updates.

Tests:

Multiple clients receive updates.

Reconnect works.

---

PHASE 4 Dashboard:

React setup.

Student board.

Cards.

Buttons.

API integration.

WebSocket integration.

Tests:

Cards move correctly.

Live updates work.

---

PHASE 5 Parent App:

React Native setup.

Home screen.

Arrival button.

Status updates.

Car registration.

Tests:

Arrival works.

Status visible.

Pickup confirmation works.

---

PHASE 6 Camera:

OpenCV capture.

Plate detection.

API client.

Cooldown logic.

Tests:

Detection triggers arrival.

Unknown handled.

No duplicate spam.

---

PHASE 7 Integration Polish:

Fix UI feedback.

Improve errors.

Add timestamps.

Detection feed.

Full demo stability.

---

PHASE 8 Demo Enhancements:

Arrival badges.

Pickup timer.

Unknown alerts.

UI polish.

Animations.

---

# AI OUTPUT REQUIREMENTS

When generating code:

Always generate complete files.

Include imports.

Include dependencies.

Include run instructions.

If modifying code:

Provide full updated file.

Do not provide fragments.

---

# SIMPLICITY RULE

Prefer simple solutions.

Avoid microservices.

Single backend service.

Single database.

Local deployment first.

Focus on workflow reliability.

Complexity only when required.

---

# FUTURE SAAS EXPANSION (DO NOT BUILD)

Authentication

Multi school support

RFID support

GPS hybrid arrival

SMS notifications

Billing

Analytics

Admin portal

Design for extensibility.

---

# MVP SUCCESS CRITERIA

MVP is complete when:

Camera detection moves student to ARRIVED.

Parent app triggers ARRIVED.

Dashboard updates live.

Teacher processes pickup.

Parent sees pickup confirmation.

Full workflow works without crashes.

System requires no manual DB edits.

Demo can be performed end to end.

---

# FINAL MISSION

Help build a convincing SaaS MVP demonstrating:

Automation

Realtime coordination

Operational efficiency

Student safety

Professional engineering quality

This system should feel like an early stage startup product.