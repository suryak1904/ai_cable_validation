import { Module } from '@nestjs/common';
import { ValidateModule } from './validate/validate.module';

@Module({
  imports: [ValidateModule],
})
export class AppModule {}
