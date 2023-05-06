public interface IDistancesService
{
  Task<DistanceMatrixResponse> GetDistanceMatrix(int fileId, bool containsHeaders, List<object> columns, DistanceMetric metric, StandarizationMethod standarization);
  string GetDistancesRequestUrl(int fileId, bool download, bool containsHeaders, List<object> columns, DistanceMetric metric, StandarizationMethod standarization);
}