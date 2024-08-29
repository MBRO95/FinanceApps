import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CommonModule } from '@angular/common';
import { RouterTestingModule } from '@angular/router/testing';

import {
  MdcTopAppBarModule,
  MdcButtonModule,
  MdcElevationModule,
  MdcIconModule,
  MdcTypographyModule,
  MdcMenuModule
} from '@angular-mdc/web';

import { ExemplarToolbarComponent } from './toolbar.component';

describe('LtwToolbarComponent', () => {
  let component: ExemplarToolbarComponent;
  let fixture: ComponentFixture<ExemplarToolbarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        CommonModule,
        RouterTestingModule,
        MdcTopAppBarModule,
        MdcButtonModule,
        MdcElevationModule,
        MdcIconModule,
        MdcTypographyModule,
        MdcMenuModule
      ],
      declarations: [ExemplarToolbarComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExemplarToolbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
