public interface IDistancesService
{
  public Task<DistanceMatrixResponse> GetDistanceMatrix(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod method);
}