(function () {
  const dateInput = document.getElementById("reservation-filter");
  const list = document.getElementById("reservation-list");
  const message = document.getElementById("reservation-message");
  const output = document.getElementById("json-output");
  const showAll = document.getElementById("show-all");
  if (!dateInput || !list) return;

  function escapeText(value) {
    return String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  }
  async function loadBookings() {
    message.textContent = "Loading reservations…";
    list.replaceChildren();
    const query = dateInput.value ? `?date=${encodeURIComponent(dateInput.value)}` : "";
    try {
      const response = await fetch(`/bookings${query}`, {headers: {"Accept":"application/json"}});
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Unable to load bookings.");
      output.textContent = JSON.stringify(data, null, 2);
      if (!data.length) {
        message.textContent = "No Booking";
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "No Booking for the selected date.";
        list.appendChild(empty);
        return;
      }
      message.textContent = `${data.length} reservation${data.length === 1 ? "" : "s"} found.`;
      data.forEach(booking => {
        const card = document.createElement("article");
        card.className = "reservation-card";
        card.innerHTML = `<div><strong>${escapeText(booking.first_name)}</strong><span>${escapeText(booking.reservation_date)}</span></div><strong>${escapeText(booking.reservation_slot)}</strong>`;
        list.appendChild(card);
      });
    } catch (error) {
      message.textContent = error.message || "Unable to load reservations.";
      output.textContent = "{}";
    }
  }
  dateInput.addEventListener("change", loadBookings);
  showAll.addEventListener("click", () => { dateInput.value = ""; loadBookings(); });
  loadBookings();
})();
