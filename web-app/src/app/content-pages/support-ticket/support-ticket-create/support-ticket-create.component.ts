import { Component } from '@angular/core';
import {
  MatDialogRef,
} from '@angular/material/dialog';
import { SupportTicketListComponent } from '../support-ticket-list/support-ticket-list.component';
import { AbstractControl, FormBuilder, FormGroup, ValidatorFn, Validators } from '@angular/forms';
import { SupportTicketServices } from '../../../core/api-services/support-ticket-services.service copy';



@Component({
  selector: 'app-support-ticket-create',
  templateUrl: './support-ticket-create.component.html',
  styleUrl: './support-ticket-create.component.scss'
})
export class SupportTicketCreateComponent {
  isClickSubmit = false;
  createSupportTicket: FormGroup;

  private minLengthTrimmed(minLength: number): ValidatorFn {
    return (control: AbstractControl): {[key: string]: any} | null => {
      const value = control.value;
      const trimmedValue = typeof value === 'string' ? value.trim() : value;
      return trimmedValue && trimmedValue.length < minLength ? {'minLengthTrimmed': {value: control.value}} : null;
    };
  }


  constructor(
    public dialogRef: MatDialogRef<SupportTicketListComponent>,
    private fb: FormBuilder,
    private supportTicketServices: SupportTicketServices,
  ) {
    this.createSupportTicket = this.fb.group({
      "name": ["", Validators.required],
      "description": ["",  [Validators.required, this.minLengthTrimmed(50)]],
      "priority": ["NORMAL", Validators.required],
      "category": ["OTHER", Validators.required],
    })
  }

  cancel(): void {
    this.dialogRef.close();
  }

  async submit() {
    this.isClickSubmit = true;

    if (this.createSupportTicket.invalid) {
      return;
    }

    const formData = this.createSupportTicket.value;
    let data = await this.supportTicketServices.createSupportTicket(formData);

    if (data.error) {
      alert(data.error);
      return;
    }

    this.dialogRef.close();
  }

}
