import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { Connectivity } from './connectivity';
import { navigation } from './navigation';

@Component({
  selector: 'app-root',
  imports: [RouterLink, RouterLinkActive, RouterOutlet, Connectivity],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  readonly navigation = navigation;
}
