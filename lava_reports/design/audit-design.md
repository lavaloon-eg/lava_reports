# Audit Create & Update – Technical Design

## Objective

Track who **created**, **updated** or **deleted** for **selected doctypes** and **specific users**.

---

## Settings Doctype

### Lava Report Settings (Single)

#### Child Tables

- **Tracked Users** User (Link → User)

- **Tracked Documents** Document Type (Link → DocType)

#### Behavior Rules

- If *Tracked Documents* is empty → **do not log anything**
- If *Tracked Users* is empty → **do not log anything**
- Settings loaded once per request (cached)

---

## Audit Log Doctype

### Lava Audit Log

| Field         | Type                           |
|---------------|--------------------------------|
| Doctype       | Data                           |
| Document Name | Data                           |
| Action        | Select (Create, Update, Delete)|
| User          | Link → User                    |
| Timestamp     | Datetime                       |

#### Permissions

- No Create / Update / Delete
- Read-only
- Visible only via report

---

## Hooks

### Applied Globally

```python
doc_events = {
  "*": {
    "on_update": "lava_report.audit.log_document_activity"
    "on_trash": "lava_report.audit.log_document_activity"
  }
}
```
