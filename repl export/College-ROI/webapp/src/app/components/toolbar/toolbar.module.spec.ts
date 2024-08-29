import { ExemplarToolbarComponentModule } from './toolbar.module';

describe('ExemplarToolbarComponentModule', () => {
  let exemplarToolbarComponentModule: ExemplarToolbarComponentModule;

  beforeEach(() => {
    exemplarToolbarComponentModule = new ExemplarToolbarComponentModule();
  });

  it('should create an instance', () => {
    expect(exemplarToolbarComponentModule).toBeTruthy();
  });
});
