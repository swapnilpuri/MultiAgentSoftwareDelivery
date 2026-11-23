import { Component } from '@angular/core';
@Component({
  selector: 'app-overview',
  template: `
    <p class="eyebrow">Workspace / Projects</p>
    <h1>Your delivery workspace</h1>
    <p>Review the foundation for governed, multi-agent software delivery.</p>
    <section class="card" aria-labelledby="foundation-title">
      <p class="eyebrow">M0 · Foundation</p>
      <h2 id="foundation-title">MultiAgentSoftwareDelivery</h2>
      <p>Standards, architecture and a connected control center.</p>
      <p>
        <strong>No managed projects yet.</strong> Project intake and persistence are planned for M1.
      </p>
      <p>Agent execution, approvals, model providers and deployments are future capabilities.</p>
    </section>
  `,
})
export class Overview {}
