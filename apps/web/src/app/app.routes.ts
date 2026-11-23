import { Routes } from '@angular/router';
import { Overview } from './overview';
import { Future } from './future';
import { navigation } from './navigation';
export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'projects' },
  { path: 'projects', component: Overview },
  ...navigation
    .slice(1)
    .map((item) => ({ path: item.path, component: Future, data: { title: item.label } })),
  { path: '**', redirectTo: 'projects' },
];
