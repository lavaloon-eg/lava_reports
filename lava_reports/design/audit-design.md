# Audit Create & Update – Technical Design

## Objective

Track who **created** or **updated** any document in Frappe for **all doctypes**, without using `track_changes`.

---

## Doctype

**Name:** Lava Audit Log

**Fields:**

- Doctype (Link → DocType)
- Document Name (Data)
- Action (Select: Create, Update)
- User (Link → User)
- Timestamp (Datetime)

---

## Hooks

Applied to all doctypes:

- `on_update` → log Create/Update (Check if new doc or not)

Exclude logging the **Lava Audit Log** doctype itself.

---

## Logging Logic

On every create or update:

- Insert one record into **Lava Audit Log**
- Store doctype, document name, action, user, timestamp

---

## Report

**Name:** Lava Audit Report  
**Type:** Query Report

**Filters:**

- Date range (mandatory)
- Document Type (optional)
- User (optional)

**Output Columns:**

- Document Type
- Document Reference
- Action
- User
- Timestamp

---

## Security

- Lava Audit Log is read-only
- Report access limited to system manager roles

---
