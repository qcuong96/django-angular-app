import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { AuthenticationGuard } from './authentication.guard';

describe('AuthenticationGuard', () => {
  let guard: AuthenticationGuard;

  beforeEach(async () => {
    await TestBed.configureTestingModule(
      {
        imports: [RouterTestingModule],
        declarations: [],
        providers: [AuthenticationGuard]
      }
    )
      .compileComponents();
  });


  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(AuthenticationGuard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
