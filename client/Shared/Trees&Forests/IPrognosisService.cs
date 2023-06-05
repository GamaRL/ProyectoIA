public interface IPrognosisService
{
  Task<PrognosisSettingsData> GetSettingsData(int fileId);
  Task SaveSettingsData(PrognosisSettingsData settings);
}