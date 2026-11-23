import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-future',
  template: `
    <p class="eyebrow">Roadmap capability</p>
    <h1>{{ title }}</h1>
    <section class="card">
      <h2>Planned for a future milestone</h2>
      <p>This section provides navigation only. No integration or execution is enabled in M0.</p>
    </section>
  `,
})
export class Future {
  readonly title = inject(ActivatedRoute).snapshot.data['title'] as string;
}
