public interface ILogisticRegressionService
{
  Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders);
  string GetImageUrl(string resource);
}