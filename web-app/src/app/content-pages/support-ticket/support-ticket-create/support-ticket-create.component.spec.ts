import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SupportTicketCreateComponent } from './support-ticket-create.component';

describe('SupportTicketCreateComponent', () => {
  let component: SupportTicketCreateComponent;
  let fixture: ComponentFixture<SupportTicketCreateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SupportTicketCreateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SupportTicketCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
