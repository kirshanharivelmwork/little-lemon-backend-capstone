(function () {
  const dateInput = document.getElementById("reservation-date");
  const slotSelect = document.getElementById("reservation-slot");
  const status = document.getElementById("slot-status");
  if (!dateInput || !slotSelect) return;

  const originalOptions = Array.from(slotSelect.options).map(o => ({value:o.value, text:o.text}));
  async function refreshSlots() {
    const selectedDate = dateInput.value;
    if (!selectedDate) return;
    const previouslySelected = slotSelect.value;
    try {
      const response = await fetch(`/available-slots/?date=${encodeURIComponent(selectedDate)}`, {
        headers: {"Accept":"application/json"}
      });
      if (!response.ok) throw new Error("Could not load available times.");
      const data = await response.json();
      slotSelect.replaceChildren();
      data.slots.forEach(slot => {
        const option = document.createElement("option");
        option.value = slot.value;
        option.textContent = slot.available ? slot.label : `${slot.label} — Booked`;
        option.disabled = !slot.available;
        slotSelect.appendChild(option);
      });
      const keep = Array.from(slotSelect.options).find(o => o.value === previouslySelected && !o.disabled);
      if (keep) keep.selected = true;
      const anyAvailable = data.slots.some(s => s.available);
      status.textContent = anyAvailable ? "Greyed-out times are already booked." : "No available slots for this date.";
      slotSelect.disabled = !anyAvailable;
    } catch (error) {
      slotSelect.replaceChildren(...originalOptions.map(item => {
        const option = document.createElement("option");
        option.value = item.value; option.textContent = item.text; return option;
      }));
      status.textContent = "Unable to refresh times. Check your connection and try again.";
      slotSelect.disabled = false;
    }
  }
  dateInput.addEventListener("change", refreshSlots);
  refreshSlots();
})();
