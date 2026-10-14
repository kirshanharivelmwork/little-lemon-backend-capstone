# Peer Review Checklist

- [ ] Admin login works in `/admin/`.
- [ ] Admin JWT token can call `GET /api/groups/manager/users`.
- [ ] Admin can assign a registered user to Manager group.
- [ ] Admin can create categories and menu items.
- [ ] Manager can obtain JWT and update item of the day.
- [ ] Manager can assign a registered user to Delivery crew group.
- [ ] Manager can assign orders to delivery crew.
- [ ] Delivery crew only sees assigned orders and can mark them delivered.
- [ ] Customer can register, obtain JWT, browse categories/menu, filter, paginate and sort.
- [ ] Customer can add/view cart, place an order, and view only their own orders.
- [ ] `python manage.py test` passes.
- [ ] `db.sqlite3` and `notes.txt` are included in the ZIP.
