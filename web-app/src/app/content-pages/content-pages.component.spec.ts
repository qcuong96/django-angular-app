import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentPagesComponent } from './content-pages.component';

describe('ContentPagesComponent', () => {
  let component: ContentPagesComponent;
  let fixture: ComponentFixture<ContentPagesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ContentPagesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ContentPagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
