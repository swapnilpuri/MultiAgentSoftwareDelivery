import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { App } from './app';
import { Connectivity } from './connectivity';
import { API_BASE_URL } from './api-config';
import { routes } from './app.routes';
import { navigation } from './navigation';

describe('Control center', () => {
  beforeEach(() =>
    TestBed.configureTestingModule({
      providers: [
        provideRouter(routes),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: API_BASE_URL, useValue: '/api/v1' },
      ],
    }),
  );
  afterEach(() => TestBed.inject(HttpTestingController).verify());
  it('renders all ten accessible navigation links', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    expect(fixture.nativeElement.querySelectorAll('nav a').length).toBe(10);
    TestBed.inject(HttpTestingController).expectOne('/api/v1/health').flush({ status: 'ok' });
    await fixture.whenStable();
    expect(fixture.nativeElement.textContent).toContain('connected');
  });
  it('shows failure and recovers on retry', async () => {
    const fixture = TestBed.createComponent(Connectivity);
    await fixture.whenStable();
    const http = TestBed.inject(HttpTestingController);
    http.expectOne('/api/v1/health').flush('offline', { status: 503, statusText: 'Unavailable' });
    await fixture.whenStable();
    expect(fixture.nativeElement.textContent).toContain('unavailable');
    fixture.nativeElement.querySelector('button').click();
    http.expectOne('/api/v1/health').flush({ status: 'ok' });
    await fixture.whenStable();
    expect(fixture.nativeElement.textContent).toContain('connected');
  });
  it('routes to overview and identifies every future capability', async () => {
    const harness = await RouterTestingHarness.create('/projects');
    expect(harness.routeNativeElement?.textContent).toContain('No managed projects yet');
    for (const item of navigation.slice(1)) {
      await harness.navigateByUrl('/' + item.path);
      expect(harness.routeNativeElement?.textContent).toContain(item.label);
      expect(harness.routeNativeElement?.textContent).toContain('future milestone');
    }
  });
});
