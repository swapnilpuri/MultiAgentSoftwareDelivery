import { Component, OnInit, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { timeout } from 'rxjs';
import { API_BASE_URL } from './api-config';
@Component({
  selector: 'app-connectivity',
  template: `<span role="status" aria-live="polite">Backend: {{ state() }}</span>
    <button
      type="button"
      (click)="check()"
      [disabled]="state() === 'checking'"
      style="margin-left: .75rem"
    >
      Retry
    </button>`,
})
export class Connectivity implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly base = inject(API_BASE_URL);
  readonly state = signal<'checking' | 'connected' | 'unavailable'>('checking');
  ngOnInit(): void {
    this.check();
  }
  check(): void {
    this.state.set('checking');
    this.http
      .get<{ status: string }>(`${this.base}/health`)
      .pipe(timeout(5000))
      .subscribe({
        next: (health) => this.state.set(health.status === 'ok' ? 'connected' : 'unavailable'),
        error: () => this.state.set('unavailable'),
      });
  }
}
