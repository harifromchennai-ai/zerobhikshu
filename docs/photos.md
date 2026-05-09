---
layout: default
title: Photo Galleries
---

## Photo Galleries

To add a new set of photos:
1. Upload your photos to the `assets/images/` folder in your repository.
2. Create a new markdown file (e.g., `gallery-new-event.md`) and add your photo links there.
3. Add a new link block below pointing to your new gallery page.

---

<a href="{{ '/gallery-madurai.html' | relative_url }}" class="photo-gallery-link">
  <h3>Madurai Guru Pooja</h3>
  <p>Click here to view photos from the Madurai Guru Pooja.</p>
</a>

<a href="{{ '/gallery-chennai.html' | relative_url }}" class="photo-gallery-link">
  <h3>Chennai Guru Pooja</h3>
  <p>Click here to view photos from the Chennai Guru Pooja.</p>
</a>

<a href="{{ '/gallery-sample.html' | relative_url }}" class="photo-gallery-link">
  <h3>Community Yoga Day</h3>
  <p>Click here to view photos from our recent community gathering.</p>
</a>